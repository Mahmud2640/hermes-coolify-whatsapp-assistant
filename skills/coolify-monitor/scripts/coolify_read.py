#!/usr/bin/env python3
"""Small, dependency-free, read-only Coolify API helper.

The script deliberately exposes a fixed set of GET requests and prints a
reduced JSON view suitable for an agent. It never prints the API token.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


TIMEOUT_SECONDS = 15
COMMANDS = {"summary", "health", "servers", "applications", "deployments"}


def _required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def _api_root() -> str:
    base = _required_env("COOLIFY_BASE_URL").rstrip("/")
    if base.endswith("/api/v1"):
        return base
    return f"{base}/api/v1"


def _get(path: str, *, authenticated: bool = True) -> Any:
    if not path.startswith("/") or ".." in path:
        raise RuntimeError("Refusing an invalid API path")

    headers = {"Accept": "application/json", "User-Agent": "coolify-monitor/1.0"}
    if authenticated:
        headers["Authorization"] = f"Bearer {_required_env('COOLIFY_API_TOKEN')}"

    request = urllib.request.Request(
        f"{_api_root()}{path}", headers=headers, method="GET"
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else None


def _pick(item: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    return {field: item.get(field) for field in fields if field in item}


def servers() -> list[dict[str, Any]]:
    data = _get("/servers") or []
    fields = (
        "name",
        "uuid",
        "reachable",
        "usable",
        "unreachable_count",
        "docker_version",
        "compose_version",
        "updated_at",
    )
    return [_pick(item, fields) for item in data if isinstance(item, dict)]


def applications() -> list[dict[str, Any]]:
    data = _get("/applications") or []
    fields = (
        "name",
        "uuid",
        "status",
        "git_branch",
        "git_commit_sha",
        "fqdn",
        "health_check_enabled",
        "updated_at",
    )
    return [_pick(item, fields) for item in data if isinstance(item, dict)]


def deployments() -> list[dict[str, Any]]:
    data = _get("/deployments") or []
    if isinstance(data, dict):
        data = data.get("data", data.get("deployments", []))
    fields = (
        "deployment_uuid",
        "resource_uuid",
        "application_name",
        "status",
        "commit",
        "commit_message",
        "created_at",
        "updated_at",
    )
    return [_pick(item, fields) for item in data if isinstance(item, dict)]


def health() -> dict[str, Any]:
    # Coolify documents /api/v1/health as a public GET endpoint. Keeping the
    # token header is harmless, but omit it to avoid sending credentials when
    # checking basic availability.
    return _get("/health", authenticated=False)


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if command not in COMMANDS:
        print(
            json.dumps(
                {"error": "unsupported_command", "allowed": sorted(COMMANDS)},
                indent=2,
            )
        )
        return 2

    try:
        if command == "servers":
            result: Any = servers()
        elif command == "applications":
            result = applications()
        elif command == "deployments":
            result = deployments()
        elif command == "health":
            result = health()
        else:
            result = {
                "servers": servers(),
                "applications": applications(),
                "running_deployments": deployments(),
            }

        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
        return 0
    except urllib.error.HTTPError as exc:
        print(
            json.dumps(
                {"error": "coolify_http_error", "status": exc.code}, indent=2
            )
        )
        return 1
    except urllib.error.URLError as exc:
        print(
            json.dumps(
                {"error": "coolify_connection_error", "reason": str(exc.reason)},
                indent=2,
            )
        )
        return 1
    except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "configuration_error", "reason": str(exc)}, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
