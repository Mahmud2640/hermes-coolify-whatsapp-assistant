# n8n artifacts

Place a **sanitized** workflow export here as:

```text
coolify-to-hermes.example.json
```

Before committing an export, remove:

- credential IDs and embedded credentials
- production webhook URLs
- phone numbers, LIDs, IP addresses, and private domains
- execution data and pinned production payloads
- real project/customer names

See [`../docs/n8n-workflow.md`](../docs/n8n-workflow.md) for the expected flow and testing checklist.
