# Troubleshooting

## Authorized WhatsApp number is rejected

Typical log:

```text
Unauthorized user: 123456789012345@lid (Example User) on whatsapp
```

WhatsApp may identify a participant with a Linked Identity Device (LID). Add both the normal phone number and the numeric LID, without `@lid`:

```env
WHATSAPP_ALLOWED_USERS=8801XXXXXXXXX,123456789012345
```

Redeploy the container, then compare the container environment with the bridge startup log:

```bash
printenv WHATSAPP_ALLOWED_USERS
grep "Allowed users:" /opt/data/whatsapp/bridge.log | tail -1
```

If the environment is new but the bridge log is old, terminate only the stale bridge and let the gateway respawn it:

```bash
pkill -f 'whatsapp-bridge.*bridge.js'
tail -30 /opt/data/whatsapp/bridge.log
```

## Environment has four users but bridge shows two

Check saved Hermes configuration for an older allowlist:

```bash
grep -RniE 'WHATSAPP_ALLOWED_USERS|allowed_users|allow_from' \
  /opt/data/config.yaml /opt/data/.env 2>/dev/null
```

Update the saved allowlist with `hermes whatsapp`, restart the gateway, and check the fresh startup line.

## Bot connects but does not answer in a group

- Confirm the sender is allowlisted.
- Confirm the group policy allows the group.
- Use WhatsApp's native mention picker; plain text such as `@bot` may not contain mention metadata.
- Confirm `WHATSAPP_REQUIRE_MENTION=true` is intentional.
- Test a DM to separate group-routing problems from model-provider problems.

## Provider returns 404 or is unavailable

Free model availability is not permanent. Select a currently available model and configure a fallback provider. Do not confuse a provider failure with WhatsApp authentication failure.

## `link-preview-js` module is missing

If the bridge still prints `WhatsApp connected!`, this dependency error may affect URL preview generation without causing the authorization problem. Pull a known-good Hermes image or repair the bridge dependencies using the Hermes-supported update procedure. Avoid ad-hoc changes that will disappear on redeploy.

## Coolify API returns 401

- Confirm API access is enabled.
- Confirm the token belongs to the correct team.
- Confirm the token has the required read permissions.
- Confirm the header is `Authorization: Bearer <token>`.
- Rotate the token if it was exposed.

## Coolify API times out from the container

- Verify `COOLIFY_BASE_URL` from inside the Hermes container.
- When Coolify is on the Docker host, use `host.docker.internal` plus the Linux `host-gateway` mapping.
- Check the Coolify API IP allowlist.
- Do not disable the firewall broadly as a shortcut.

## `running:unknown`

This is not automatically a confirmed outage. It normally means the platform lacks a usable application health signal. Report it as unknown and verify the application endpoint or configure an appropriate healthcheck.
