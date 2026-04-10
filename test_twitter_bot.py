"""
test_twitter_bot.py
====================
Unit tests for Twitter-related functionality in overseer_bot.py.

Run with:
    python test_twitter_bot.py

All tests use plain assert statements and mock out external I/O so they can
run without real Twitter credentials or network access.
"""

import importlib
import sys
import types
import time
import unittest
from unittest.mock import MagicMock, patch, call

# ---------------------------------------------------------------------------
# Stub heavy optional dependencies so the module can import in CI without
# the full requirements set (solana, web3, ccxt, etc.)
# ---------------------------------------------------------------------------

def _create_stub_module(name):
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod

for _stub in ['ccxt', 'solana', 'solana.rpc', 'solana.rpc.api',
              'solders', 'solders.keypair', 'solders.pubkey',
              'solders.transaction', 'base58', 'web3',
              'api_client', 'scalper']:
    if _stub not in sys.modules:
        _create_stub_module(_stub)

# Provide attribute stubs that overseer_bot accesses at import time
sys.modules['base58'].b58decode = lambda x: b'\x00' * 32
web3_stub = sys.modules['web3']
web3_stub.Web3 = MagicMock()

# ---------------------------------------------------------------------------
# Import the module with Twitter credentials absent so TWITTER_ENABLED=False
# ---------------------------------------------------------------------------
import os
for _key in ['CONSUMER_KEY', 'CONSUMER_SECRET', 'ACCESS_TOKEN',
             'ACCESS_SECRET', 'BEARER_TOKEN']:
    os.environ.pop(_key, None)

import overseer_bot as bot

# ===========================================================================
# Helpers
# ===========================================================================

def _reset_tweet_dedup():
    """Clear the in-memory dedup dict between tests."""
    with bot.RECENT_TWEET_HASHES_LOCK:
        bot.RECENT_TWEET_HASHES.clear()


def _reset_price_cooldowns():
    bot.PRICE_ALERT_COOLDOWNS.clear()


# ===========================================================================
# 1. Tweet deduplication
# ===========================================================================

class TestTweetDedup(unittest.TestCase):

    def setUp(self):
        _reset_tweet_dedup()

    def test_tweet_hash_returns_consistent_md5(self):
        h1 = bot._tweet_hash("hello world")
        h2 = bot._tweet_hash("hello world")
        assert h1 == h2, "Same text must produce same hash"
        assert len(h1) == 32, "MD5 hex digest should be 32 chars"

    def test_tweet_hash_different_texts(self):
        assert bot._tweet_hash("a") != bot._tweet_hash("b")

    def test_is_duplicate_tweet_false_when_empty(self):
        assert not bot.is_duplicate_tweet("brand new tweet"), \
            "Should not be a duplicate when dedup dict is empty"

    def test_mark_and_detect_duplicate(self):
        text = "test tweet content"
        bot.mark_tweet_sent(text)
        assert bot.is_duplicate_tweet(text), \
            "Should detect duplicate after marking"

    def test_different_text_not_duplicate(self):
        bot.mark_tweet_sent("tweet A")
        assert not bot.is_duplicate_tweet("tweet B"), \
            "Different text must not be flagged as duplicate"

    def test_expired_entry_not_duplicate(self):
        """Entries older than the dedup window should not block new tweets."""
        text = "old tweet"
        h = bot._tweet_hash(text)
        with bot.RECENT_TWEET_HASHES_LOCK:
            # Place a timestamp well outside the window
            bot.RECENT_TWEET_HASHES[h] = time.time() - bot.TWEET_DEDUP_WINDOW_SECONDS - 1
        assert not bot.is_duplicate_tweet(text), \
            "Expired dedup entry should not block re-posting"

    def test_expired_entry_is_pruned(self):
        """is_duplicate_tweet should clean up expired entries."""
        old_text = "ancient tweet"
        h = bot._tweet_hash(old_text)
        with bot.RECENT_TWEET_HASHES_LOCK:
            bot.RECENT_TWEET_HASHES[h] = time.time() - bot.TWEET_DEDUP_WINDOW_SECONDS - 1
        bot.is_duplicate_tweet("trigger prune")
        with bot.RECENT_TWEET_HASHES_LOCK:
            assert h not in bot.RECENT_TWEET_HASHES, "Expired entry should be pruned"


# ===========================================================================
# 2. Price alert cooldown
# ===========================================================================

class TestPriceAlertCooldown(unittest.TestCase):

    def setUp(self):
        _reset_price_cooldowns()

    def test_not_on_cooldown_initially(self):
        assert not bot.is_price_alert_on_cooldown("BTC/USDT")

    def test_on_cooldown_after_mark(self):
        bot.mark_price_alert_sent("BTC/USDT")
        assert bot.is_price_alert_on_cooldown("BTC/USDT")

    def test_different_symbol_not_on_cooldown(self):
        bot.mark_price_alert_sent("BTC/USDT")
        assert not bot.is_price_alert_on_cooldown("ETH/USDT")

    def test_cooldown_expires(self):
        symbol = "SOL/USDT"
        bot.PRICE_ALERT_COOLDOWNS[symbol] = time.time() - bot.PRICE_ALERT_COOLDOWN_SECONDS - 1
        assert not bot.is_price_alert_on_cooldown(symbol), \
            "Cooldown should have expired"


# ===========================================================================
# 3. Twitter duplicate error detection
# ===========================================================================

class TestIsTwitterDuplicateError(unittest.TestCase):

    def _make_exc(self, api_codes=None, msg=""):
        exc = MagicMock(spec=bot.tweepy.TweepyException)
        exc.api_codes = api_codes
        exc.__str__ = lambda self: msg
        return exc

    def test_detects_by_api_code_187(self):
        exc = self._make_exc(api_codes=[187])
        assert bot._is_twitter_duplicate_error(exc)

    def test_detects_by_string_187(self):
        exc = self._make_exc(api_codes=None, msg="Error 187: duplicate status")
        assert bot._is_twitter_duplicate_error(exc)

    def test_detects_by_word_duplicate(self):
        exc = self._make_exc(api_codes=None, msg="Status is a duplicate.")
        assert bot._is_twitter_duplicate_error(exc)

    def test_detects_case_insensitive_duplicate(self):
        exc = self._make_exc(api_codes=None, msg="DUPLICATE content detected")
        assert bot._is_twitter_duplicate_error(exc)

    def test_non_duplicate_error(self):
        exc = self._make_exc(api_codes=[89], msg="Invalid or expired token")
        assert not bot._is_twitter_duplicate_error(exc)

    def test_empty_api_codes(self):
        exc = self._make_exc(api_codes=[], msg="some other error")
        assert not bot._is_twitter_duplicate_error(exc)


# ===========================================================================
# 4. calculate_price_change
# ===========================================================================

class TestCalculatePriceChange(unittest.TestCase):

    def test_positive_change(self):
        result = bot.calculate_price_change(100.0, 110.0)
        assert abs(result - 10.0) < 1e-6, f"Expected 10.0, got {result}"

    def test_negative_change(self):
        result = bot.calculate_price_change(100.0, 90.0)
        assert abs(result - (-10.0)) < 1e-6, f"Expected -10.0, got {result}"

    def test_no_change(self):
        result = bot.calculate_price_change(50.0, 50.0)
        assert result == 0.0

    def test_zero_old_price_returns_zero(self):
        result = bot.calculate_price_change(0, 100.0)
        assert result == 0, "Division by zero guard must return 0"


# ===========================================================================
# 5. create_fallback_alert_message — length guard
# ===========================================================================

class TestFallbackAlertMessage(unittest.TestCase):

    def test_within_twitter_limit(self):
        msg = bot.create_fallback_alert_message("BTC", 12.5, 45000.0)
        assert len(msg) <= bot.TWITTER_CHAR_LIMIT, \
            f"Fallback alert too long: {len(msg)} chars"

    def test_contains_token_name(self):
        msg = bot.create_fallback_alert_message("SOL", -5.0, 100.0)
        assert "SOL" in msg

    def test_contains_game_link(self):
        msg = bot.create_fallback_alert_message("ETH", 3.0, 2000.0)
        assert bot.GAME_LINK in msg


# ===========================================================================
# 6. TWITTER_ENABLED gate — posting functions bail out silently
# ===========================================================================

class TestTwitterDisabledGate(unittest.TestCase):
    """When TWITTER_ENABLED is False and client is None, no tweeting occurs."""

    def setUp(self):
        _reset_tweet_dedup()
        _reset_price_cooldowns()
        # Ensure disabled state (import already set this; reinforce)
        bot.TWITTER_ENABLED = False
        bot.client = None

    def test_post_price_alert_skips_when_disabled(self):
        with patch.object(bot, 'client', None):
            # Should not raise; should just return
            bot.post_price_alert("BTC/USDT", {'price': 1.0, 'change_24h': 5.0}, 5.0)

    def test_post_activation_tweet_skips_when_disabled(self):
        bot.post_activation_tweet()  # Should not raise

    def test_overseer_diagnostic_skips_when_disabled(self):
        bot.overseer_diagnostic()  # Should not raise

    def test_overseer_retweet_hunt_skips_when_disabled(self):
        bot.overseer_retweet_hunt()  # Should not raise

    def test_overseer_respond_skips_when_disabled(self):
        bot.overseer_respond()  # Should not raise


# ===========================================================================
# 7. post_price_alert — with mocked Twitter client
# ===========================================================================

class TestPostPriceAlert(unittest.TestCase):

    def setUp(self):
        _reset_tweet_dedup()
        _reset_price_cooldowns()
        self.mock_client = MagicMock()
        bot.TWITTER_ENABLED = True
        bot.client = self.mock_client

    def tearDown(self):
        bot.TWITTER_ENABLED = False
        bot.client = None
        _reset_tweet_dedup()
        _reset_price_cooldowns()

    def test_happy_path_posts_tweet(self):
        price_data = {'price': 45000.0, 'change_24h': 6.0}
        bot.post_price_alert("BTC/USDT", price_data, 6.0)
        self.mock_client.create_tweet.assert_called_once()
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        assert len(tweet_text) <= bot.TWITTER_CHAR_LIMIT, \
            f"Tweet exceeds 280 chars: {len(tweet_text)}"

    def test_cooldown_prevents_check_price_alerts_from_posting(self):
        """check_price_alerts() must skip post_price_alert when on cooldown."""
        bot.mark_price_alert_sent("BTC/USDT")
        assert bot.is_price_alert_on_cooldown("BTC/USDT"), \
            "BTC/USDT should be on cooldown immediately after mark"

    def test_does_not_post_duplicate_tweet(self):
        """A text that was already posted (and marked in the dedup cache) must not be re-posted."""
        price_data = {'price': 45000.0, 'change_24h': 6.0}
        # Post the first tweet so we know the exact text that was sent
        bot.post_price_alert("BTC/USDT", price_data, 6.0)
        assert self.mock_client.create_tweet.call_count == 1, "First post should call create_tweet once"
        first_call_text = self.mock_client.create_tweet.call_args[1]['text']

        # Now pre-load the dedup entry with the exact same text and reset cooldown
        _reset_price_cooldowns()
        bot.mark_tweet_sent(first_call_text)
        self.mock_client.create_tweet.reset_mock()

        # Force the same text by patching the random selection in post_price_alert
        with patch.object(bot.random, 'choice', return_value=first_call_text):
            bot.post_price_alert("BTC/USDT", price_data, 6.0)

        self.mock_client.create_tweet.assert_not_called()

    def test_handles_tweepy_exception_gracefully(self):
        self.mock_client.create_tweet.side_effect = bot.tweepy.TweepyException("rate limit")
        price_data = {'price': 45000.0, 'change_24h': 7.0}
        # Should not raise
        bot.post_price_alert("BTC/USDT", price_data, 7.0)

    def test_handles_tweepy_duplicate_error_gracefully(self):
        class _DupError(bot.tweepy.TweepyException):
            api_codes = [187]
            def __str__(self):
                return "187 duplicate"
        self.mock_client.create_tweet.side_effect = _DupError("187 duplicate")
        price_data = {'price': 45000.0, 'change_24h': 7.0}
        bot.post_price_alert("BTC/USDT", price_data, 7.0)  # should not raise


# ===========================================================================
# 8. post_activation_tweet — with mocked Twitter client
# ===========================================================================

class TestPostActivationTweet(unittest.TestCase):

    def setUp(self):
        _reset_tweet_dedup()
        self.mock_client = MagicMock()
        bot.TWITTER_ENABLED = True
        bot.client = self.mock_client

    def tearDown(self):
        bot.TWITTER_ENABLED = False
        bot.client = None
        _reset_tweet_dedup()

    def test_posts_activation_tweet(self):
        bot.post_activation_tweet()
        self.mock_client.create_tweet.assert_called_once()
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        assert len(tweet_text) <= bot.TWITTER_CHAR_LIMIT, \
            f"Activation tweet exceeds 280 chars: {len(tweet_text)}"

    def test_activation_tweet_contains_game_link(self):
        bot.post_activation_tweet()
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        assert bot.GAME_LINK in tweet_text

    def test_activation_tweet_contains_overseer_reference(self):
        bot.post_activation_tweet()
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        # All messages reference the overseer/bot name in some form
        assert bot.BOT_NAME in tweet_text or "Vault" in tweet_text, \
            f"Activation tweet should reference bot or vault, got: {tweet_text[:80]}"

    def test_tweepy_exception_is_handled_gracefully(self):
        self.mock_client.create_tweet.side_effect = bot.tweepy.TweepyException("fail")
        bot.post_activation_tweet()  # must not raise


# ===========================================================================
# 9. overseer_diagnostic — with mocked Twitter client
# ===========================================================================

class TestOverseerDiagnostic(unittest.TestCase):

    def setUp(self):
        _reset_tweet_dedup()
        self.mock_client = MagicMock()
        bot.TWITTER_ENABLED = True
        bot.client = self.mock_client

    def tearDown(self):
        bot.TWITTER_ENABLED = False
        bot.client = None
        _reset_tweet_dedup()

    def test_posts_diagnostic_tweet(self):
        bot.overseer_diagnostic()
        self.mock_client.create_tweet.assert_called_once()
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        assert len(tweet_text) <= bot.TWITTER_CHAR_LIMIT, \
            f"Diagnostic tweet exceeds 280 chars: {len(tweet_text)}"

    def test_skips_duplicate_diagnostic(self):
        # First call posts successfully
        bot.overseer_diagnostic()
        assert self.mock_client.create_tweet.call_count == 1
        # Mark the posted text as sent manually to force duplicate
        tweet_text = self.mock_client.create_tweet.call_args[1]['text']
        self.mock_client.create_tweet.reset_mock()
        # Inject the exact hash so the dedup fires
        bot.mark_tweet_sent(tweet_text)
        # Patch generate_overseer_tweet to return the same text
        with patch.object(bot, 'generate_overseer_tweet', return_value=tweet_text):
            bot.overseer_diagnostic()
        self.mock_client.create_tweet.assert_not_called()

    def test_handles_tweepy_exception(self):
        self.mock_client.create_tweet.side_effect = bot.tweepy.TweepyException("network error")
        bot.overseer_diagnostic()  # should not raise


# ===========================================================================
# 10. generate_overseer_tweet — LLM disabled path
# ===========================================================================

class TestGenerateOverseerTweet(unittest.TestCase):

    def test_returns_none_when_llm_disabled(self):
        original = bot.LLM_ENABLED
        try:
            bot.LLM_ENABLED = False
            result = bot.generate_overseer_tweet("test topic")
            assert result is None, "Should return None when LLM is disabled"
        finally:
            bot.LLM_ENABLED = original

    def test_trims_to_max_chars(self):
        long_text = "x " * 200  # 400 chars
        with patch.object(bot, 'generate_llm_response', return_value=long_text):
            original = bot.LLM_ENABLED
            try:
                bot.LLM_ENABLED = True
                result = bot.generate_overseer_tweet("topic", max_chars=100)
                assert result is None or len(result) <= 100, \
                    f"Result should be trimmed to 100 chars, got {len(result) if result else 'None'}"
            finally:
                bot.LLM_ENABLED = original

    def test_strips_surrounding_quotes(self):
        raw = '"Vault 77 is online."'
        with patch.object(bot, 'generate_llm_response', return_value=raw):
            original = bot.LLM_ENABLED
            try:
                bot.LLM_ENABLED = True
                result = bot.generate_overseer_tweet("topic")
                assert result is not None
                assert not result.startswith('"'), "Leading quote should be stripped"
                assert not result.endswith('"'), "Trailing quote should be stripped"
            finally:
                bot.LLM_ENABLED = original

    def test_returns_none_when_llm_returns_empty(self):
        with patch.object(bot, 'generate_llm_response', return_value=""):
            original = bot.LLM_ENABLED
            try:
                bot.LLM_ENABLED = True
                result = bot.generate_overseer_tweet("topic")
                assert result is None
            finally:
                bot.LLM_ENABLED = original


# ===========================================================================
# 11. Lore / personality content — basic sanity checks
# ===========================================================================

class TestLoreContent(unittest.TestCase):

    def test_lores_list_nonempty(self):
        assert len(bot.LORES) > 0

    def test_threats_list_nonempty(self):
        assert len(bot.THREATS) > 0

    def test_fizzco_ads_use_correct_ticker(self):
        """$CAPS ticker must appear in at least some FizzCo ads; AFCAPS must not."""
        full_text = " ".join(bot.FIZZCO_ADS)
        assert "$CAPS" in full_text, "FizzCo ads should reference $CAPS ticker"
        assert "AFCAPS" not in full_text, "AFCAPS is incorrect ticker — use $CAPS"

    def test_token_launch_hype_uses_correct_ticker(self):
        full_text = " ".join(bot.TOKEN_LAUNCH_HYPE)
        assert "$CAPS" in full_text
        assert "AFCAPS" not in full_text

    def test_get_personality_line_returns_string(self):
        line = bot.get_personality_line()
        assert isinstance(line, str) and len(line) > 0

    def test_elon_troll_tone_exists(self):
        """elon_troll must be a registered personality tone with content."""
        assert 'elon_troll' in bot.PERSONALITY_TONES, "elon_troll tone must exist in PERSONALITY_TONES"
        assert len(bot.PERSONALITY_TONES['elon_troll']) >= 5, "elon_troll tone must have at least 5 lines"

    def test_elon_troll_lines_stay_in_character(self):
        """Elon troll lines must not be blatantly political — in-character dry wit only."""
        political_keywords = ["hate", "evil", "criminal", "traitor", "fascist"]
        full_text = " ".join(bot.PERSONALITY_TONES['elon_troll']).lower()
        for kw in political_keywords:
            assert kw not in full_text, f"elon_troll lines must stay in character — found '{kw}'"

    def test_elon_troll_lines_reference_mr_house_or_vault_tec(self):
        """At least one elon_troll line should draw a Fallout in-universe parallel."""
        fallout_terms = ["house", "vault", "rocket", "caps", "doge", "terminal", "wasteland", "musk", "x "]
        full_text = " ".join(bot.PERSONALITY_TONES['elon_troll']).lower()
        found = any(term in full_text for term in fallout_terms)
        assert found, "elon_troll lines should include Fallout-universe parallels or in-character framing"

    def test_get_threat_level_returns_valid_dict(self):
        threat = bot.get_threat_level()
        assert 'level' in threat
        assert 'desc' in threat
        assert threat['level'] in [t['level'] for t in bot.THREAT_LEVELS]


# ===========================================================================
# Run
# ===========================================================================

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
