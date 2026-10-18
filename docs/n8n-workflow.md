# n8n workflow

## Recommended flow

```text
Webhook Trigger
  -> Normalize Event
  -> Validate Required Fields
  -> Build Notification Text
  -> Generate HMAC-SHA256
  -> HTTP Request to Hermes
  -> Respond to Webhook
```

## Input normalization

Keep only fields needed by operators:

```json
{
  "event": "deployment_success",
  "project": "example-project",
  "environment": "production",
  "resource": "example-app",
  "status": "success",
  "branch": "main",
  "commit": "short-sha",
  "commit_message": "Sanitized one-line summary",
  "actor": "deployment-user",
  "timestamp": "2026-01-01T00:00:00Z"
}
```

Do not forward environment values, authorization headers, tokens, full Git payloads, or customer data.

## Signature

Generate an HMAC-SHA256 signature over the **exact raw body** sent to Hermes, using `WEBHOOK_SECRET`. The secret stored in n8n must match the Hermes secret. Do not hard-code it in a workflow exported to GitHub.

## Delivery modes

Choose one:

- **Direct/deliver-only:** recommended for routine success/failure notifications. No LLM cost and deterministic formatting.
- **Agent-backed:** use when the event needs summarization or a follow-up skill call. Treat every payload field as untrusted.

## Message template

```text
🔔 Coolify Notification

Event: {{event}}
Project: {{project}}
Environment: {{environment}}
Resource: {{resource}}
Branch: {{branch}}
Status: {{status}}
Commit: {{commit}} — {{commit_message}}
Actor: {{actor}}
Time: {{timestamp}}
```

## Exporting for this repository

1. Export the completed workflow from n8n as JSON.
2. Remove credential IDs, webhook production URLs, phone numbers, domains, IP addresses, and sample production payloads.
3. Replace secrets with expressions such as `$env.WEBHOOK_SECRET`.
4. Save it as `n8n/coolify-to-hermes.example.json`.
5. Import the sanitized copy into a clean n8n instance and test it before publishing.
