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

# Send a Telegram message with images
send_telegram_message(
    chat_id="-1001234567890",
    token="your-bot-token",
    text="Chart update",
    image_paths=["/path/to/chart.png"]
)

# Send a Discord message
send_discord_message(
    webhook_url="https://discord.com/api/webhooks/...",
    content="Hello from your bot!"
)
```

## API Reference

### `send_telegram_message(chat_id, token, text, image_paths)`

Sends a text message (and optional images) to a Telegram chat using the Bot API.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chat_id` | `str` | required | Target chat ID (group, channel, or private) |
| `token` | `str` | required | Telegram bot token from @BotFather |
| `text` | `str` | `""` | Message content. Long messages are split automatically |
| `image_paths` | `list[str]` | `None` | Local file paths of images to send after the text |

### `send_discord_message(webhook_url, content, image_paths, logger)`

Posts a message to a Discord channel via webhook.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `webhook_url` | `str` | required | Discord webhook URL |
| `content` | `str` | required | Message content. Long messages are split automatically |
| `image_paths` | `list[str]` | `None` | Local file paths of images to attach |
| `logger` | `Callable` | `None` | Optional callback for logging send status |

## Links

- [PyPI](https://pypi.org/project/awesome-notify-bridge/)
- [Repository](https://github.com/trunghvbk-afataw/notify-bridge)
- [Report an Issue](https://github.com/trunghvbk-afataw/notify-bridge/issues)
