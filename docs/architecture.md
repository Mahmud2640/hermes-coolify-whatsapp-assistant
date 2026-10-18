# Architecture

## Overview

The solution separates event delivery from interactive monitoring. Both paths end in WhatsApp, but only interactive questions invoke the language model and Coolify skill.

## Push notification path

```mermaid
sequenceDiagram
    participant C as Coolify
    participant N as n8n
    participant H as Hermes Webhook
    participant W as WhatsApp Group

    C->>N: Deployment/resource event
    N->>N: Normalize and redact payload
    N->>N: Generate HMAC signature
    N->>H: Signed POST /webhooks/coolify-events
    H->>W: Rendered notification
```

Use Hermes `deliver-only` mode for deterministic notifications that do not need reasoning. It is faster and consumes no model tokens. Use an agent-backed route only when the event genuinely needs interpretation or enrichment.

## Interactive monitoring path

```mermaid
sequenceDiagram
    participant U as Authorized User
    participant W as WhatsApp Bridge
    participant G as Hermes Gateway
    participant S as Coolify Monitor Skill
    participant A as Coolify API

    U->>W: Native mention + question
    W->>G: Authorized message
    G->>S: Invoke read-only skill
    S->>A: GET servers/applications/deployments
    A-->>S: JSON state
    S-->>G: Sanitized JSON summary
    G-->>W: Human-readable answer
    W-->>U: WhatsApp reply
```

## Trust boundaries

| Boundary | Control |
|---|---|
| WhatsApp sender to Hermes | Explicit phone/LID allowlist and mention requirement |
| Internet to Hermes webhook | HTTPS and HMAC signature verification |
| Hermes to Coolify | Least-privilege bearer token and GET-only helper |
| Event payload to agent | Treat payload content as untrusted data |
| Repository to public GitHub | Placeholders, `.gitignore`, redacted media, secret scan |

## Design decisions

- **Dedicated WhatsApp number:** reduces the impact of an unofficial bridge restriction.
- **Read-only monitoring skill:** avoids accidental deployments or downtime.
- **n8n normalization:** prevents vendor-specific payload fields from leaking directly into notifications.
- **HMAC signatures:** detect altered or forged webhook requests.
- **Home channel delivery:** keeps scheduled and event-driven operational messages in one group.
