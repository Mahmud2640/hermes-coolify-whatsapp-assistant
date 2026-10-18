# Security policy

## Supported scope

This repository provides documentation and example configuration. It does not host a public service and does not include production credentials.

## Reporting a vulnerability

Please report a suspected vulnerability privately to the repository owner. Do not include working credentials, WhatsApp session files, private payloads, customer data, or internal infrastructure details in a public issue.

## Before publishing a fork

- Rotate any credential that has appeared in a terminal, screenshot, chat, or Git history.
- Never commit `.env`, `auth.json`, `creds.json`, WhatsApp session data, API tokens, webhook secrets, QR codes, or unredacted logs.
- Use a least-privilege Coolify token and keep the monitoring skill read-only.
- Require an HMAC signature on the Hermes webhook.
- Allowlist specific WhatsApp users; do not use `*` for a private operations bot.
- Require a native group mention before invoking the agent.
- Keep the Hermes webhook behind HTTPS.
- Enable GitHub secret scanning and push protection on a public repository.

If a secret is committed, deleting the file in a later commit is insufficient. Revoke or rotate the secret immediately and remove it from Git history before publishing.
