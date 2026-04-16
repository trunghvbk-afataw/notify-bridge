from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Callable

import requests


MAX_DISCORD_LENGTH = 2000
DISCORD_HTTP_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "NotifyBridge/1.0 (+https://discord.com)",
}

LoggerFn = Callable[[str], None]


def _post_discord_json(webhook_url: str, payload: dict, logger: LoggerFn | None = None) -> bool:
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers=DISCORD_HTTP_HEADERS,
            timeout=10,
        )
        ok = 200 <= response.status_code < 300
        if logger:
            logger(f"Discord send: {response.status_code} {response.reason}")
        return ok
    except Exception as exc:
        if logger:
            logger(f"Failed to send Discord message: {exc}")
        return False


def _post_discord_file(webhook_url: str, payload: dict, image_path: str, logger: LoggerFn | None = None) -> bool:
    file_path = Path(image_path)
    if not file_path.exists():
        if logger:
            logger(f"Discord image not found, skipping: {image_path}")
        return False
    try:
        mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        with file_path.open("rb") as file_handle:
            files = {"files[0]": (file_path.name, file_handle, mime_type)}
            response = requests.post(
                webhook_url,
                data={"payload_json": json.dumps(payload, ensure_ascii=False)},
                files=files,
                headers=DISCORD_HTTP_HEADERS,
                timeout=20,
            )
        ok = 200 <= response.status_code < 300
        if logger:
            logger(f"Discord file send: {response.status_code} {response.reason} file={file_path.name}")
        return ok
    except Exception as exc:
        if logger:
            logger(f"Failed to send Discord file {file_path.name}: {exc}")
        return False


def _split_discord_message(text: str) -> list[str]:
    if len(text) <= MAX_DISCORD_LENGTH:
        return [text]
    chunks = []
    while text:
        if len(text) <= MAX_DISCORD_LENGTH:
            chunks.append(text)
            break
        cut = text.rfind("\n", 0, MAX_DISCORD_LENGTH)
        if cut <= 0:
            cut = MAX_DISCORD_LENGTH
        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")
    return chunks


def send_discord_message(
    webhook_url: str,
    content: str,
    image_paths: list[str] | None = None,
    logger: LoggerFn | None = None,
) -> bool:
    if not webhook_url:
        if logger:
            logger("Discord webhook_url is empty, skipping send.")
        return False

    image_paths = image_paths or []
    payload_base = {"allowed_mentions": {"parse": []}}
    chunks = _split_discord_message(content)
    all_ok = True

    for chunk in chunks:
        payload = dict(payload_base)
        payload["content"] = chunk
        all_ok = _post_discord_json(webhook_url, payload, logger=logger) and all_ok

    for image_path in image_paths:
        all_ok = _post_discord_file(webhook_url, dict(payload_base), image_path, logger=logger) and all_ok

    return all_ok
