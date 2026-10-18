---
name: coolify-monitor
description: Read-only Coolify monitoring for questions about servers, applications, deployments, resource health, and failed releases.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [coolify, monitoring, server, deployment, devops]
    category: devops
    requires_toolsets: [terminal]
---

# Coolify Monitor

Use this skill when an authorized user asks about Coolify servers, applications, projects, health, failures, or active deployments.

## Allowed operation

Run only the bundled sanitized read-only helper:

```text
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py summary
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py servers
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py applications
python /opt/data/skills/devops/coolify-monitor/scripts/coolify_read.py deployments
```

The helper only performs GET requests against a fixed endpoint allowlist.

## Response rules

1. Lead with the number of confirmed problems.
2. Treat `failed`, `exited`, `unhealthy`, and unreachable servers as problems.
3. Treat `running:unknown` as unknown, not as a confirmed failure.
4. State when an application has no configured healthcheck.
5. Include application name, branch/environment, status, and update time when available.
6. Never print credentials, authorization headers, raw environment values, or private API responses.
7. Reply in the language used by the user.

## Prohibited operations

Do not deploy, restart, stop, delete, patch, validate, mutate, or execute arbitrary URLs or commands. If the user requests a write operation, explain that this monitoring skill is intentionally read-only.
