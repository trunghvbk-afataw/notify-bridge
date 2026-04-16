# notify-bridge

Reusable notification helpers for Telegram Bot API and Discord webhook.

## Install

```bash
pip install notify-bridge
```

For local development:

```bash
pip install -e .[dev]
```

## Usage

```python
from notify_bridge import send_discord_message, send_telegram_message

send_discord_message(webhook_url="https://discord.com/api/webhooks/...", content="Hello from bot")
send_telegram_message(chat_id="-1001234567890", token="<bot-token>", text="Hello from bot")
```

## Design Notes

- The package stays project-agnostic: no hardcoded env var names or app-specific wrappers.
- Each consuming project should map its own configuration into `send_telegram_message(...)` and `send_discord_message(...)`.
- Project-specific helpers such as `send_signal()` or `send_hourly()` should live outside this package.

## Release

Build and validate the package locally:

```bash
python -m pip install -e .[dev]
python -m pytest
python -m build
python -m twine check dist/*
```

Upload to PyPI after creating an API token:

```bash
python -m twine upload dist/*
```
