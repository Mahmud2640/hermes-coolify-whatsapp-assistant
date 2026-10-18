# Security checklist

## Credentials

- Create a dedicated Coolify API token for this integration.
- Grant only read permissions needed for monitoring.
- Store secrets in Coolify/n8n credential storage, not workflow JSON or Compose source.
- Use a long, randomly generated webhook secret.
- Rotate credentials immediately if they appear in screenshots, logs, chat, or Git history.

## Network

- Serve the Hermes webhook only over HTTPS.
- Restrict Coolify API source IPs where deployment networking permits it.
- Do not publish the Coolify admin interface merely to make container networking easier.
- Prefer an internal address such as `host.docker.internal` when Hermes and Coolify share a host.

## WhatsApp

- Use a dedicated number rather than a personal account.
- Allowlist only trusted operators.
- Keep group mention gating enabled.
- Add a numeric LID only after identifying it from trusted local logs.
- Never commit `creds.json`, QR codes, or session mapping files.

## Agent and tools

- Keep the Coolify skill GET-only.
- Do not expose deploy, restart, stop, delete, terminal, or file-write operations to webhook-triggered runs.
- Prefer `deliver-only` for routine notifications.
- Consider webhook payloads, commit messages, resource names, and log text untrusted.
- Do not allow an event payload to select arbitrary tools, commands, files, URLs, or recipients.

## GitHub publication

- Enable secret scanning and push protection.
- Review `git diff --cached` before every commit.
- Search for common secret patterns before the first push.
- Redact screenshots and flatten image metadata where appropriate.
- Keep an example environment file; never commit the real `.env`.
