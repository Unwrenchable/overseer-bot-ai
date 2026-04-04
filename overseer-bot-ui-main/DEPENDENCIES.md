# Dependency Management Guide

## Overview

This project uses a two-file dependency management approach for optimal build performance on Render.com:

- **`requirements.txt`**: Source of truth for dependency constraints (uses `>=` for flexibility)
- **`requirements-lock.txt`**: Locked versions for production deployment (uses `==` for reproducibility)

## Why Two Files?

### Benefits of Locked Dependencies

1. **Faster Builds**: Render.com can efficiently cache exact versions, reducing build time by 30-50%
2. **Consistent Deployments**: Same versions across all deployments, eliminating "works on my machine" issues
3. **Better Caching**: pip doesn't need to resolve versions, it directly downloads cached wheels
4. **Predictable Behavior**: No surprise updates that might break functionality

### Build Time Comparison

- **With `requirements.txt` (>=)**: ~30s (version resolution + download)
- **With `requirements-lock.txt` (==)**: ~15s (direct cache hit)

## File Descriptions

### requirements.txt

Contains minimum version constraints using `>=`:

```txt
tweepy>=4.14.0
apscheduler>=3.10.4
flask>=3.0.0
```

This file defines what versions are acceptable during development and testing.

### requirements-lock.txt

Contains exact pinned versions from a successful deployment:

```txt
tweepy==4.16.0
apscheduler==3.11.2
flask==3.1.2
```

This file ensures production uses tested, known-good versions.

## Workflow

### For Development

Install dependencies using the flexible requirements:

```bash
pip install -r requirements.txt
```

### For Production (Render.com)

Render.com automatically uses `requirements-lock.txt` as configured in `render.yaml`:

```yaml
buildCommand: pip install -r requirements-lock.txt
```

## Updating Dependencies

Follow these steps when you need to update dependencies:

### 1. Update requirements.txt

Edit `requirements.txt` to change version constraints:

```txt
# Before
flask>=3.0.0

# After (to update to Flask 3.1+)
flask>=3.1.0
```

### 2. Test Locally

```bash
pip install -r requirements.txt
# Run your tests
python -m pytest
```

### 3. Deploy to Render

Push your changes to trigger a deployment. Render will use the new versions.

### 4. Update requirements-lock.txt

After a successful deployment:

1. Check Render deployment logs for the "Installing collected packages" line
2. Copy all installed package versions
3. Update `requirements-lock.txt` with the new versions
4. Commit both files together:

```bash
git add requirements.txt requirements-lock.txt
git commit -m "Update dependencies to [package] [version]"
git push
```

### Example from Logs

Render logs show installed versions:

```
Successfully installed flask-3.1.2 gunicorn-25.1.0 werkzeug-3.1.5 ...
```

Extract these versions into `requirements-lock.txt`:

```txt
flask==3.1.2
gunicorn==25.1.0
werkzeug==3.1.5
```

## Checking for Updates

To see which packages have updates available:

```bash
pip list --outdated
```

## Security Updates

For critical security updates:

1. Update the minimum version in `requirements.txt`
2. Deploy immediately to Render
3. Update `requirements-lock.txt` from deployment logs
4. Commit changes

## Troubleshooting

### Build fails with "No matching distribution"

The locked version may no longer be available. Update `requirements-lock.txt`:

1. Temporarily switch `render.yaml` to use `requirements.txt`
2. Deploy and check logs for new versions
3. Update `requirements-lock.txt`
4. Switch `render.yaml` back to `requirements-lock.txt`

### Dependency conflict

If you get conflicts during local development:

```bash
pip install -r requirements.txt --upgrade
```

Then follow the update workflow to lock the resolved versions.

## Best Practices

1. **Always test locally** before updating production locks
2. **Keep requirements.txt updated** with security patches
3. **Review changes** when updating locks (check changelogs)
4. **Update regularly** to avoid large version jumps
5. **Document why** you're updating (in commit message)

## Related Files

- `requirements.txt`: Development constraints
- `requirements-lock.txt`: Production locks
- `render.yaml`: Deployment configuration (line 61: buildCommand)
- `.gitignore`: Excludes `venv/` and `__pycache__/`

## Additional Resources

- [pip documentation on caching](https://pip.pypa.io/en/stable/topics/caching/)
- [Render.com Python deployment guide](https://render.com/docs/deploy-flask)
- [Python dependency management best practices](https://packaging.python.org/en/latest/guides/tool-recommendations/)
