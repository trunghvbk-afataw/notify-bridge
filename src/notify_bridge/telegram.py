from __future__ import annotations

import json
import mimetypes
import uuid
from pathlib import Path
from urllib import error, request
from urllib.parse import urlencode


MAX_TEXT_LENGTH = 4096


def _build_multipart(fields: dict[str, str], file_field: str, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----NotifyBridgeBoundary{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    lines = []
    for key, value in fields.items():
        lines.append(f"--{boundary}")
        lines.append(f'Content-Disposition: form-data; name="{key}"')
        lines.append("")
        lines.append(value)

    lines.append(f"--{boundary}")
    lines.append(f'Content-Disposition: form-data; name="{file_field}"; filename="{file_path.name}"')
    lines.append(f"Content-Type: {mime_type}")
    lines.append("")
    head = "\r\n".join(lines).encode("utf-8") + b"\r\n"
    tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = head + file_bytes + tail
    return body, f"multipart/form-data; boundary={boundary}"


def _send_json(token: str, method: str, payload: dict) -> dict:
    endpoint = f"https://api.telegram.org/bot{token}/{method}"
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=35) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram {method} failed ({exc.code}): {raw}") from exc
    if not data.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {data}")
    return data["result"]


def _send_file(token: str, method: str, file_field: str, chat_id: str, file_path: Path, caption: str = "") -> dict:
    endpoint = f"https://api.telegram.org/bot{token}/{method}"
    fields = {"chat_id": chat_id}
    if caption:
        fields["caption"] = caption
    body, content_type = _build_multipart(fields, file_field, file_path)
    req = request.Request(endpoint, data=body, headers={"Content-Type": content_type}, method="POST")
    try:
        with request.urlopen(req, timeout=35) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram {method} failed ({exc.code}): {raw}") from exc
    if not data.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {data}")
    return data["result"]


def _chat_id_candidates(chat_id: str) -> list[str]:
    normalized = (chat_id or "").strip()
    if not normalized:
        return [normalized]
    candidates = [normalized]
    if normalized.startswith("-") and not normalized.startswith("-100"):
        abs_id = normalized[1:]
        if abs_id.isdigit():
            candidates.append(f"-100{abs_id}")
    return candidates


def chat_id_matches(expected_chat_id: str, actual_chat_id: str | int) -> bool:
    actual = str(actual_chat_id).strip()
    expected_candidates = {candidate.strip() for candidate in _chat_id_candidates(expected_chat_id)}
    return actual in expected_candidates


def fetch_telegram_updates(
    token: str,
    *,
    offset: int | None = None,
    timeout_seconds: int = 0,
    allowed_updates: list[str] | None = None,
) -> list[dict]:
    endpoint = f"https://api.telegram.org/bot{token}/getUpdates"
    payload: dict[str, object] = {
        "timeout": max(0, int(timeout_seconds)),
    }
    if offset is not None:
        payload["offset"] = int(offset)
    if allowed_updates:
        payload["allowed_updates"] = allowed_updates
    query = urlencode(payload, doseq=True)
    url = f"{endpoint}?{query}" if query else endpoint
    req = request.Request(url, method="GET")
    try:
        with request.urlopen(req, timeout=max(35, timeout_seconds + 5)) as response:
            data = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Telegram getUpdates failed ({exc.code}): {raw}") from exc
    if not data.get("ok"):
        raise RuntimeError(f"Telegram getUpdates failed: {data}")
    return data.get("result", [])


def extract_update_text(update: dict) -> tuple[str | None, dict | None]:
    message = update.get("message") or update.get("edited_message")
    if not isinstance(message, dict):
        return None, None
    text = message.get("text")
    if isinstance(text, str):
        return text.strip(), message
    return None, message


def _split_text(text: str, limit: int = MAX_TEXT_LENGTH) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        cut = text.rfind("\n", 0, limit)
        if cut <= 0:
            cut = limit
        chunks.append(text[:cut])
        text = text[cut:].lstrip("\n")
    return chunks


def send_telegram_message(chat_id: str, token: str, text: str = "", image_paths: list[str] | None = None) -> dict:
    image_paths = image_paths or []
    last_error: Exception | None = None
    for chat_candidate in _chat_id_candidates(chat_id):
        sent_items = []
        try:
            if text:
                for chunk in _split_text(text):
                    result = _send_json(
                        token,
                        "sendMessage",
                        {"chat_id": chat_candidate, "text": chunk, "disable_web_page_preview": True},
                    )
                    sent_items.append({"type": "text", "message_id": str(result.get("message_id", ""))})
            for image_path in image_paths:
                result = _send_file(token, "sendPhoto", "photo", chat_candidate, Path(image_path))
                sent_items.append({"type": "photo", "path": image_path, "message_id": str(result.get("message_id", ""))})
            return {"status": "sent", "chat_id_used": chat_candidate, "sent_items": sent_items}
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    return {"status": "sent", "sent_items": []}
