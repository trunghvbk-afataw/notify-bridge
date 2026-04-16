# awesome-notify-bridge

Simple notification helpers for sending messages via **Telegram Bot API** and **Discord webhooks**.

## Installation

```bash
pip install awesome-notify-bridge
```

## Quick Start

```python
from notify_bridge import send_telegram_message, send_discord_message

# Send a Telegram message
send_telegram_message(
    chat_id="-1001234567890",
    token="your-bot-token",
    text="Hello from your bot!"
)

# Send a Discord message
send_discord_message(
    webhook_url="https://discord.com/api/webhooks/...",
    content="Hello from your bot!"
)
```

## API Reference

### `send_telegram_message(chat_id, token, text, **kwargs)`

Sends a text message to a Telegram chat using the Bot API.

| Parameter | Type | Description |
|-----------|------|-------------|
| `chat_id` | `str` | Target chat ID (group, channel, or private) |
| `token` | `str` | Telegram bot token from @BotFather |
| `text` | `str` | Message content |

### `send_discord_message(webhook_url, content, **kwargs)`

Posts a message to a Discord channel via webhook.

| Parameter | Type | Description |
|-----------|------|-------------|
| `webhook_url` | `str` | Discord webhook URL |
| `content` | `str` | Message content |

## Links

- [PyPI](https://pypi.org/project/awesome-notify-bridge/)
- [Repository](https://github.com/trunghvbk-afataw/notify-bridge)
- [Report an Issue](https://github.com/trunghvbk-afataw/notify-bridge/issues)
