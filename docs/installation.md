# Installation

This guide assumes a working Coolify instance and a dedicated WhatsApp number. Commands and paths may vary by Hermes version.

## 1. Prepare Coolify API access

1. Enable API access in the Coolify instance settings.
2. Restrict the allowed API source IPs where practical.
3. Create a team API token with the minimum permissions required to list servers, applications, and deployments.
4. Test from the Hermes container:

```bash
python -c "import os,urllib.request; u=os.environ['COOLIFY_BASE_URL'].rstrip('/')+'/api/v1/health'; print(urllib.request.urlopen(u,timeout=10).status)"
```

Expected result: `200`.

## 2. Deploy Hermes

Use `docker-compose.example.yml` as a starting point. Store secrets in Coolify's environment-variable manager rather than in the Compose file.

Required values:

| Variable | Purpose |
|---|---|
| `WHATSAPP_ALLOWED_USERS` | Authorized phone numbers and, when necessary, numeric LID aliases |
| `WHATSAPP_HOME_CHANNEL_NAME` | Human-readable target group name |
| `WEBHOOK_SECRET` | HMAC secret shared with n8n |
| `COOLIFY_BASE_URL` | Trusted Coolify origin without `/api/v1` |
| `COOLIFY_API_TOKEN` | Least-privilege API token |

Deploy the service and confirm the container is running. A healthcheck is optional; a missing healthcheck is not itself a failure.

## 3. Pair the dedicated WhatsApp number

Open the Hermes container terminal:

```bash
hermes whatsapp
```

Choose bot/separate-number mode and scan the QR code from **WhatsApp > Linked devices** on the dedicated phone. Do not publish or screenshot the QR code.

Verify the bridge:

```bash
tail -30 /opt/data/whatsapp/bridge.log
```

Look for `WhatsApp connected!` and the expected allowed users.

## 4. Create the operations group

1. Create a private WhatsApp group.
2. Add the dedicated bot number and authorized operators.
3. Send `/sethome` in the group if requested by Hermes.
4. Keep `WHATSAPP_REQUIRE_MENTION=true` so ordinary conversation does not invoke the agent.
5. Test with a native WhatsApp mention, not plain `@bot` text.

## 5. Install the Coolify skill

Copy the repository skill directory into the persistent Hermes data volume:

```text
/opt/data/skills/devops/coolify-monitor/
```

Verify:

```bash
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py summary
```

The output must contain only read-only status data and must never print the API token.

## 6. Configure the webhook

Enable the Hermes webhook listener on port `8644`, publish it through HTTPS, and verify:

```text
GET https://your-hermes-domain.example/health
```

Expected response:

```json
{"status":"ok","platform":"webhook"}
```

Create the Hermes webhook route and configure n8n using [n8n-workflow.md](n8n-workflow.md).

## 7. Acceptance tests

- Authorized DM receives a reply.
- Unauthorized DM is ignored or rejected.
- Group message without a mention does not trigger Hermes.
- Native mention triggers one reply.
- Coolify test notification reaches the group.
- `summary` returns current servers, applications, and deployments.
- A test webhook with an invalid signature is rejected.
- Restarting/redeploying Hermes preserves the WhatsApp session volume.
