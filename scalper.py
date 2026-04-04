"""
Token Scalper Module for Overseer Bot
======================================
Scans Solana DEX pools for new token listings and rug pull signals.
Runs as two daemon background threads inside the same process as overseer_bot.py.

Discovery:   DexScreener token-profiles API  (no auth, 300 req/min free tier)
Safety:      rugcheck.xyz report API         (no auth, Solana tokens)
Rug monitor: DexScreener pairs API           (liquidity change tracking)
Alerts:      Callback functions injected at start() to avoid circular imports
"""
from __future__ import annotations

import os
import time
import logging
import threading
import requests

# -------------------------------------------------------
# CONFIGURATION  (all tunable via environment variables)
# -------------------------------------------------------
ENABLE_SCALPER = os.getenv('ENABLE_SCALPER', 'true').lower() == 'true'

# How often to look for brand-new token listings (seconds)
SCALPER_SCAN_INTERVAL = int(os.getenv('SCALPER_SCAN_INTERVAL', '120'))

# How often to re-check watched pools for rug-pull signals (seconds)
SCALPER_POOL_MONITOR_INTERVAL = int(os.getenv('SCALPER_POOL_MONITOR_INTERVAL', '300'))

# Liquidity drop threshold to trigger a rug-pull alert (percent)
SCALPER_RUG_LIQUIDITY_THRESHOLD = float(os.getenv('SCALPER_RUG_LIQUIDITY_THRESHOLD', '50.0'))

# Minimum opportunity score (0-100) required before posting a high-potential alert
SCALPER_MIN_OPPORTUNITY_SCORE = int(os.getenv('SCALPER_MIN_OPPORTUNITY_SCORE', '70'))

# Maximum number of pools to watch simultaneously
SCALPER_MAX_WATCHED_POOLS = int(os.getenv('SCALPER_MAX_WATCHED_POOLS', '50'))

# Minimum liquidity (USD) for a token to be considered for high-potential alert
SCALPER_MIN_LIQUIDITY_USD = float(os.getenv('SCALPER_MIN_LIQUIDITY_USD', '5000'))

# Cooldown between alerts for the same token (seconds)
SCALPER_ALERT_COOLDOWN = int(os.getenv('SCALPER_ALERT_COOLDOWN', '3600'))

# DexScreener API base URL
DEXSCREENER_API = 'https://api.dexscreener.com'

# rugcheck.xyz API
RUGCHECK_API_BASE = 'https://api.rugcheck.xyz/v1'
RUGCHECK_TIMEOUT = 10

# HTTP request timeout for DexScreener calls
DEXSCREENER_TIMEOUT = 8

# -------------------------------------------------------
# MODULE STATE  (thread-safe via _state_lock)
# -------------------------------------------------------
_scanner_thread: threading.Thread | None = None
_monitor_thread: threading.Thread | None = None
_stop_event = threading.Event()

_seen_token_addresses: set[str] = set()   # DexScreener tokenAddress values already processed
_watched_pools: dict[str, dict] = {}       # tokenAddress -> pool metadata
_alert_cooldowns: dict[str, float] = {}    # tokenAddress -> last_alert_timestamp

_state_lock = threading.Lock()

# In-process caches
_rugcheck_cache: dict[str, dict] = {}      # mint -> {ts, data}
_dexscreener_cache: dict[str, dict] = {}   # tokenAddress -> {ts, data}

RUGCHECK_CACHE_TTL = 3600    # 1 hour
DEXSCREENER_CACHE_TTL = 120  # 2 minutes

# Callbacks — injected by start()
_callbacks: dict[str, object] = {}


# -------------------------------------------------------
# DEXSCREENER HELPERS
# -------------------------------------------------------

def _dexscreener_get(path: str) -> dict | list | None:
    """GET a DexScreener API path and return parsed JSON, or None on error."""
    try:
        resp = requests.get(f"{DEXSCREENER_API}{path}", timeout=DEXSCREENER_TIMEOUT)
        if resp.status_code == 200:
            return resp.json()
        logging.debug(f"[SCALPER] DexScreener {path} → HTTP {resp.status_code}")
    except Exception as e:
        logging.debug(f"[SCALPER] DexScreener request failed ({path}): {e}")
    return None


def get_latest_token_profiles() -> list[dict]:
    """
    Fetch the latest token profiles from DexScreener.
    Returns a list of profile dicts each containing at minimum:
        chainId, tokenAddress, description
    """
    data = _dexscreener_get('/token-profiles/latest/v1')
    if isinstance(data, list):
        return data
    return []


def get_token_pairs(token_address: str) -> list[dict]:
    """
    Fetch DEX pair data for a token address from DexScreener.
    Returns a list of pair dicts; each has 'liquidity', 'volume', 'priceChange', etc.
    """
    now = time.time()
    if token_address in _dexscreener_cache:
        cached = _dexscreener_cache[token_address]
        if now - cached['ts'] < DEXSCREENER_CACHE_TTL:
            return cached['data']

    data = _dexscreener_get(f'/latest/dex/tokens/{token_address}')
    pairs = []
    if isinstance(data, dict):
        pairs = data.get('pairs') or []
    _dexscreener_cache[token_address] = {'ts': now, 'data': pairs}
    return pairs


def _best_pair(pairs: list[dict]) -> dict | None:
    """Return the pair with the highest USD liquidity."""
    if not pairs:
        return None
    return max(pairs, key=lambda p: float((p.get('liquidity') or {}).get('usd') or 0))


# -------------------------------------------------------
# RUGCHECK SAFETY CHECK
# -------------------------------------------------------

def check_solana_token_safety(mint_address: str) -> dict:
    """
    Check Solana token safety via rugcheck.xyz.

    Returns:
        is_safe (bool)
        risk_score (int)  — rugcheck 0-1000+ scale; >500 is risky
        risks (list[str]) — human-readable risk labels
        name (str)
        symbol (str)
        mint_authority_disabled (bool)
        freeze_authority_disabled (bool)
    """
    now = time.time()
    if mint_address in _rugcheck_cache:
        cached = _rugcheck_cache[mint_address]
        if now - cached['ts'] < RUGCHECK_CACHE_TTL:
            return cached['data']

    result: dict = {
        'is_safe': True,
        'risk_score': 0,
        'risks': [],
        'name': '',
        'symbol': '',
        'mint_authority_disabled': False,
        'freeze_authority_disabled': False,
    }

    try:
        url = f"{RUGCHECK_API_BASE}/tokens/{mint_address}/report/summary"
        resp = requests.get(url, timeout=RUGCHECK_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            score = int(data.get('score', 0))
            risks_raw = data.get('risks') or []

            result['risk_score'] = score
            result['is_safe'] = score < 500
            result['risks'] = [
                r.get('description') or r.get('name', '')
                for r in risks_raw
                if r.get('description') or r.get('name')
            ]

            meta = data.get('tokenMeta') or {}
            result['name'] = meta.get('name', '')
            result['symbol'] = meta.get('symbol', '')

            # Absence of 'mint' / 'freeze' in risk names is a good sign
            risk_names_lower = ' '.join(r.get('name', '').lower() for r in risks_raw)
            result['mint_authority_disabled'] = 'mint' not in risk_names_lower
            result['freeze_authority_disabled'] = 'freeze' not in risk_names_lower
        else:
            result['risks'].append(f'Safety check unavailable (HTTP {resp.status_code})')
    except Exception as e:
        logging.debug(f"[SCALPER] rugcheck failed for {mint_address}: {e}")
        result['risks'].append('Safety check unavailable')

    _rugcheck_cache[mint_address] = {'ts': now, 'data': result}
    return result


# -------------------------------------------------------
# OPPORTUNITY SCORING
# -------------------------------------------------------

def calculate_opportunity_score(safety: dict, liquidity_usd: float) -> tuple[int, list[str]]:
    """
    Score a newly discovered token 0-100 for opportunity potential.
    Returns (score, reasons_list).
    """
    score = 0
    reasons: list[str] = []

    risk = safety.get('risk_score', 1000)

    # Safety (max 40 pts)
    if risk < 100:
        score += 40
        reasons.append('Very low risk score')
    elif risk < 300:
        score += 25
        reasons.append('Low risk score')
    elif risk < 500:
        score += 10
        reasons.append('Moderate risk score')

    # Mint authority revoked (max 20 pts)
    if safety.get('mint_authority_disabled'):
        score += 20
        reasons.append('Mint authority disabled')

    # Freeze authority revoked (max 10 pts)
    if safety.get('freeze_authority_disabled'):
        score += 10
        reasons.append('Freeze authority disabled')

    # Liquidity (max 30 pts)
    if liquidity_usd >= 50_000:
        score += 30
        reasons.append(f'Strong liquidity (${liquidity_usd:,.0f})')
    elif liquidity_usd >= 10_000:
        score += 20
        reasons.append(f'Moderate liquidity (${liquidity_usd:,.0f})')
    elif liquidity_usd >= SCALPER_MIN_LIQUIDITY_USD:
        score += 10
        reasons.append(f'Liquidity (${liquidity_usd:,.0f})')

    return min(score, 100), reasons


# -------------------------------------------------------
# ALERT HELPERS
# -------------------------------------------------------

def _risk_score_to_severity(risk_score: int) -> str:
    if risk_score >= 700:
        return 'critical'
    if risk_score >= 500:
        return 'high'
    if risk_score >= 300:
        return 'medium'
    return 'low'


def _is_on_cooldown(token_address: str) -> bool:
    with _state_lock:
        last = _alert_cooldowns.get(token_address, 0)
    return time.time() - last < SCALPER_ALERT_COOLDOWN


def _set_cooldown(token_address: str) -> None:
    with _state_lock:
        _alert_cooldowns[token_address] = time.time()


def _fire(event: str, data: dict) -> None:
    """Invoke a registered callback safely."""
    cb = _callbacks.get(event)
    if cb:
        try:
            cb(data)
        except Exception as e:
            logging.error(f"[SCALPER] Callback '{event}' raised: {e}")
    else:
        logging.debug(f"[SCALPER] No callback for '{event}'; event data: {data.get('token_name', '')}")


def _make_token_display(name: str, symbol: str, address: str) -> str:
    short = f"{address[:8]}...{address[-4:]}" if len(address) >= 12 else address
    if symbol:
        return f"${symbol} ({short})"
    if name:
        return f"{name} ({short})"
    return short


# -------------------------------------------------------
# NEW TOKEN SCANNER
# -------------------------------------------------------

def scan_for_new_tokens() -> None:
    """
    Fetch the latest DexScreener token profiles and process any Solana tokens
    we haven't seen yet.  Runs safety checks and fires alerts via callbacks.
    """
    profiles = get_latest_token_profiles()
    if not profiles:
        logging.debug('[SCALPER] No token profiles returned from DexScreener')
        return

    # Filter to tokens we haven't seen yet
    new_profiles: list[dict] = []
    with _state_lock:
        for p in profiles:
            addr = p.get('tokenAddress', '')
            if addr and addr not in _seen_token_addresses:
                _seen_token_addresses.add(addr)
                new_profiles.append(p)

    if not new_profiles:
        logging.debug('[SCALPER] No new token profiles in this scan batch')
        return

    logging.info(f'[SCALPER] {len(new_profiles)} new token profile(s) to evaluate')

    for profile in new_profiles:
        chain_id = profile.get('chainId', '')
        token_address = profile.get('tokenAddress', '')

        if not token_address:
            continue

        # Fetch pair data for liquidity information
        pairs = get_token_pairs(token_address)
        best = _best_pair(pairs)
        liquidity_usd = float((best or {}).get('liquidity', {}).get('usd') or 0)

        # Skip tokens with no meaningful liquidity
        if liquidity_usd < SCALPER_MIN_LIQUIDITY_USD:
            logging.debug(f'[SCALPER] Skipping {token_address[:16]}... — liquidity too low (${liquidity_usd:.0f})')
            time.sleep(0.3)
            continue

        base = (best or {}).get('baseToken') or {}
        token_name = base.get('name', '')
        token_symbol = base.get('symbol', '')
        token_display = _make_token_display(token_name, token_symbol, token_address)

        logging.info(f'[SCALPER] Evaluating {token_display} — liquidity ${liquidity_usd:,.0f} — chain {chain_id}')

        # Solana safety check via rugcheck.xyz; EVM tokens get a simplified pass-through
        if chain_id == 'solana':
            safety = check_solana_token_safety(token_address)
        else:
            # For non-Solana tokens rely solely on DexScreener signals
            safety = {
                'is_safe': True,
                'risk_score': 0,
                'risks': [],
                'name': token_name,
                'symbol': token_symbol,
                'mint_authority_disabled': False,
                'freeze_authority_disabled': False,
            }

        score, reasons = calculate_opportunity_score(safety, liquidity_usd)

        if not safety['is_safe']:
            # High-risk / scam token — fire rug pull alert
            if not _is_on_cooldown(token_address):
                detail = '; '.join(safety['risks'][:3]) or 'High risk indicators detected'
                _fire('on_rug_pull', {
                    'type': 'rug_pull',
                    'token_name': token_display,
                    'token_address': token_address,
                    'severity': _risk_score_to_severity(safety['risk_score']),
                    'details': detail,
                })
                _set_cooldown(token_address)
                logging.warning(f'[SCALPER] Rug/scam alert fired for {token_display} (risk {safety["risk_score"]})')

        elif score >= SCALPER_MIN_OPPORTUNITY_SCORE:
            # Promising new token
            if not _is_on_cooldown(token_address):
                _fire('on_high_potential', {
                    'type': 'high_potential',
                    'token_name': token_display,
                    'token_address': token_address,
                    'opportunity_score': score,
                    'reasons': reasons,
                })
                _set_cooldown(token_address)
                logging.info(f'[SCALPER] High-potential alert fired for {token_display} (score {score}/100)')

                # Start watching this pool for rug signals
                if best:
                    pair_address = best.get('pairAddress', '')
                    with _state_lock:
                        if len(_watched_pools) < SCALPER_MAX_WATCHED_POOLS:
                            _watched_pools[token_address] = {
                                'pair_address': pair_address,
                                'initial_liquidity_usd': liquidity_usd,
                                'last_liquidity_usd': liquidity_usd,
                                'first_seen': time.time(),
                                'score': score,
                                'name': token_display,
                                'chain_id': chain_id,
                            }
        else:
            logging.debug(f'[SCALPER] {token_display} scored {score}/100 — below threshold, not alerting')

        time.sleep(0.5)  # be polite to APIs between tokens


# -------------------------------------------------------
# POOL LIQUIDITY MONITOR
# -------------------------------------------------------

def monitor_watched_pools() -> None:
    """
    Re-fetch liquidity for all watched pools and fire rug-pull alerts
    when liquidity drops by more than SCALPER_RUG_LIQUIDITY_THRESHOLD %.
    """
    with _state_lock:
        pool_snapshot = dict(_watched_pools)

    if not pool_snapshot:
        return

    logging.debug(f'[SCALPER] Monitoring {len(pool_snapshot)} watched pool(s)...')

    mints_to_remove: list[str] = []

    for token_address, pool in pool_snapshot.items():
        pairs = get_token_pairs(token_address)
        best = _best_pair(pairs)
        current_liquidity = float((best or {}).get('liquidity', {}).get('usd') or 0)

        if current_liquidity == 0:
            # DexScreener may have dropped the pair — stop watching after 24h
            age = time.time() - pool['first_seen']
            if age > 86400:
                mints_to_remove.append(token_address)
            continue

        initial = pool['initial_liquidity_usd']
        if initial <= 0:
            continue

        # Update last known value
        with _state_lock:
            if token_address in _watched_pools:
                _watched_pools[token_address]['last_liquidity_usd'] = current_liquidity

        pct_change = ((current_liquidity - initial) / initial) * 100

        if pct_change <= -SCALPER_RUG_LIQUIDITY_THRESHOLD:
            if not _is_on_cooldown(token_address):
                drop = abs(pct_change)
                severity = 'critical' if drop >= 90 else 'high' if drop >= 70 else 'medium'
                _fire('on_rug_pull', {
                    'type': 'rug_pull',
                    'token_name': pool['name'],
                    'token_address': token_address,
                    'severity': severity,
                    'details': (
                        f'Liquidity dropped {drop:.0f}%'
                        f' (${initial:,.0f} → ${current_liquidity:,.0f})'
                    ),
                })
                _set_cooldown(token_address)
                logging.warning(
                    f'[SCALPER] Rug-pull detected: {pool["name"]} '
                    f'liquidity −{drop:.0f}% (${initial:,.0f} → ${current_liquidity:,.0f})'
                )
            mints_to_remove.append(token_address)  # stop watching after rug

        elif time.time() - pool['first_seen'] > 86400:
            # Older than 24 h — retire from watch list
            mints_to_remove.append(token_address)

        time.sleep(0.3)  # rate-limit RPC calls

    if mints_to_remove:
        with _state_lock:
            for addr in mints_to_remove:
                _watched_pools.pop(addr, None)


# -------------------------------------------------------
# BACKGROUND THREADS
# -------------------------------------------------------

def _scanner_loop() -> None:
    logging.info(f'[SCALPER] Token scanner thread started (interval: {SCALPER_SCAN_INTERVAL}s)')
    while not _stop_event.is_set():
        try:
            scan_for_new_tokens()
        except Exception as e:
            logging.error(f'[SCALPER] Scanner loop error: {e}')
        _stop_event.wait(SCALPER_SCAN_INTERVAL)
    logging.info('[SCALPER] Token scanner thread stopped')


def _monitor_loop() -> None:
    logging.info(f'[SCALPER] Pool monitor thread started (interval: {SCALPER_POOL_MONITOR_INTERVAL}s)')
    # Initial delay so scanner runs first and populates watched pools
    _stop_event.wait(SCALPER_POOL_MONITOR_INTERVAL)
    while not _stop_event.is_set():
        try:
            monitor_watched_pools()
        except Exception as e:
            logging.error(f'[SCALPER] Monitor loop error: {e}')
        _stop_event.wait(SCALPER_POOL_MONITOR_INTERVAL)
    logging.info('[SCALPER] Pool monitor thread stopped')


# -------------------------------------------------------
# PUBLIC API
# -------------------------------------------------------

def start(
    on_rug_pull=None,
    on_high_potential=None,
    on_airdrop=None,
) -> None:
    """
    Start the token scalper background threads.

    Args:
        on_rug_pull:      Callable(alert_data) invoked for rug-pull events.
        on_high_potential: Callable(alert_data) invoked for high-potential tokens.
        on_airdrop:       Callable(alert_data) invoked for airdrop events.
    """
    global _scanner_thread, _monitor_thread

    if not ENABLE_SCALPER:
        logging.info('[SCALPER] Disabled via ENABLE_SCALPER=false — skipping startup')
        return

    if _scanner_thread and _scanner_thread.is_alive():
        logging.warning('[SCALPER] start() called but threads are already running — skipping')
        return

    if on_rug_pull:
        _callbacks['on_rug_pull'] = on_rug_pull
    if on_high_potential:
        _callbacks['on_high_potential'] = on_high_potential
    if on_airdrop:
        _callbacks['on_airdrop'] = on_airdrop

    _stop_event.clear()

    _scanner_thread = threading.Thread(
        target=_scanner_loop, name='scalper-scanner', daemon=True
    )
    _scanner_thread.start()

    _monitor_thread = threading.Thread(
        target=_monitor_loop, name='scalper-monitor', daemon=True
    )
    _monitor_thread.start()

    logging.info('☢️  [SCALPER] Token scalper module started — watching the wasteland for new tokens ☢️')


def stop() -> None:
    """Gracefully stop the scalper background threads (blocks up to 10 s)."""
    _stop_event.set()
    for t in (_scanner_thread, _monitor_thread):
        if t and t.is_alive():
            t.join(timeout=5)
    logging.info('[SCALPER] Stopped')


def get_status() -> dict:
    """Return current runtime status for the monitoring dashboard."""
    with _state_lock:
        watched = len(_watched_pools)
        seen = len(_seen_token_addresses)
        cooldowns = len(_alert_cooldowns)

    return {
        'enabled': ENABLE_SCALPER,
        'scanner_running': bool(_scanner_thread and _scanner_thread.is_alive()),
        'monitor_running': bool(_monitor_thread and _monitor_thread.is_alive()),
        'watched_pools': watched,
        'seen_tokens': seen,
        'active_cooldowns': cooldowns,
        'scan_interval_seconds': SCALPER_SCAN_INTERVAL,
        'pool_monitor_interval_seconds': SCALPER_POOL_MONITOR_INTERVAL,
        'min_opportunity_score': SCALPER_MIN_OPPORTUNITY_SCORE,
        'rug_liquidity_threshold_pct': SCALPER_RUG_LIQUIDITY_THRESHOLD,
    }
