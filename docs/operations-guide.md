# Operations guide

This is the day-to-day guide for using and checking the assistant after installation.

## How to talk to the assistant

In a group, select the assistant using WhatsApp's native mention picker and then ask the question:

```text
@bot Are all servers healthy?
@bot কোন application failed হয়েছে?
@bot testing branch-এর current status কী?
@bot এখন কোনো deployment চলছে?
```

Continue by replying to the assistant's message when you want the existing conversation context to remain clear.

The expected language behavior is:

- Bengali question → Bengali response
- Banglish question → natural Banglish response
- English question → English response
- The operator is addressed as “Sir” unless they request otherwise

## What a good status response should contain

1. Confirmed problem count first
2. Server reachability and usability
3. Applications with failed/exited/unhealthy status
4. Applications with unknown health, listed separately
5. Currently running deployments
6. Timestamp or last update when available

The assistant must not claim that everything is healthy if some applications have no reliable health signal.

## Routine verification

### Check the container-level allowlist

```bash
printenv WHATSAPP_ALLOWED_USERS
```

### Check the allowlist used by the bridge

```bash
grep "Allowed users:" /opt/data/whatsapp/bridge.log | tail -1
```

These values should represent the same authorized identities. If they differ, follow the stale-bridge procedure in [troubleshooting](troubleshooting.md).

### Check WhatsApp connectivity

```bash
tail -30 /opt/data/whatsapp/bridge.log
```

Expected:

```text
WhatsApp connected!
```

### Check Coolify API reachability

```bash
python -c "import os,urllib.request; u=os.environ['COOLIFY_BASE_URL'].rstrip('/')+'/api/v1/health'; print(urllib.request.urlopen(u,timeout=10).status)"
```

Expected:

```text
200
```

### Check the monitoring skill

```bash
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py summary
```

Expected top-level keys:

```json
{
  "servers": [],
  "applications": [],
  "running_deployments": []
}
```

The arrays may be empty depending on the environment, but the command should not print the bearer token.

### Check the public webhook

Open:

```text
https://your-hermes-domain.example/health
```

Expected:

```json
{"status":"ok","platform":"webhook"}
```

## How to interpret common states

| State | Meaning | Recommended response |
|---|---|---|
| `running:healthy` | Process is running and the reported health is good | No action required |
| `running:unknown` | Process may be running but health is not reliably known | Report as unknown; verify endpoint/healthcheck |
| `exited:unhealthy` | Process exited and health failed | Investigate application/deployment logs |
| Server `reachable=false` | Coolify cannot reach the server | Treat as an incident |
| No running deployments | Nothing is actively deploying | Normal unless a deployment was expected |
| `Running (no healthcheck)` | Container is running without an additional health assertion | Not automatically a failure |

## Notification expectations

At minimum, enable notifications for:

- deployment failure
- server unreachable
- restart limit reached
- disk usage warning
- backup failure
- scheduled task failure

Success notifications can be useful during initial validation but may become noisy. For a production group, keep failure and warning events immediate and consider summarizing routine successes.

## When the assistant takes too long

The WhatsApp connection and Coolify API may be healthy while the model provider is slow.

1. Read the progress message.
2. If the provider is retrying repeatedly, send `/stop`.
3. Select another available model with `/model`.
4. Retry the original request.
5. Configure a fallback provider for long-term reliability.

## After changing configuration

Use this order:

1. Save the Compose/environment changes.
2. Redeploy/recreate the container when environment variables changed.
3. Confirm the effective variable with `printenv`.
4. Confirm the child bridge started with the new value in its log.
5. Send one controlled test message.
6. Check fresh logs by timestamp.

Do not assume a UI save, process restart, container recreation, and bridge respawn are the same operation.

## Weekly maintenance

- Test one interactive status question.
- Confirm one signed test notification.
- Review repeated provider failures.
- Review unauthorized-user warnings.
- Confirm the Coolify token has not gained write permissions.
- Review disk usage and backup failure notifications.
- Update Hermes deliberately and record the version before and after.
- Keep a recent backup of the persistent Hermes data volume, protecting session files as secrets.

## Incident notes template

```text
Time:
Observed symptom:
Affected component:
Last known successful test:
Relevant sanitized log line:
Container environment verified: yes/no
Bridge configuration verified: yes/no
Coolify API verified: yes/no
Model provider verified: yes/no
Action taken:
Result:
Follow-up:
```

This prevents unrelated problems—such as provider downtime and WhatsApp authorization—from being diagnosed as the same failure.
