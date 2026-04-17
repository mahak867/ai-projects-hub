# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest (main) | ✅ |

## API Key Safety

**Never commit your API keys.** This repo is configured to prevent accidental leaks:

- `.gitignore` excludes `.env` files
- Every project uses `.env.example` (safe to commit) instead of `.env` (never commit)
- The CI checks that no `.env` files are tracked

If you accidentally commit a key:
1. **Immediately revoke it** at [console.anthropic.com](https://console.anthropic.com)
2. Generate a new one
3. Remove it from git history: `git filter-branch` or `git filter-repo`

## Reporting a Vulnerability

If you find a security issue in this repo (e.g. a pattern that teaches unsafe practices, a script that could expose credentials, or a dependency with a known CVE):

1. **Do not open a public issue**
2. Email: *(add your email here)*
3. Include: what the issue is, which file/line, and a suggested fix

You'll get a response within 48 hours. If the issue is valid, it will be fixed and you'll be credited in the changelog.

## Dependency Security

All projects pin minimum versions in `requirements.txt`. To check for known vulnerabilities:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

## Safe Usage Reminders

- The trading signals projects (13, 17) are for **educational paper trading only** — not financial advice
- The computer use demo (10) runs bash commands in a **restricted allowlist** — do not expand it without understanding the risks
- The WhatsApp bot (03) stores conversations **in memory only** — no data persists after restart
