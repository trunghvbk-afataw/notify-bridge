from pathlib import Path

from notify_bridge import discord


def test_split_discord_message_prefers_newlines() -> None:
    chunks = discord._split_discord_message("first\nsecond\nthird",)

    assert chunks == ["first\nsecond\nthird"]


def test_split_discord_message_respects_limit() -> None:
    chunks = discord._split_discord_message("abcde\nfghij\nklmno"[:],)

    assert chunks == ["abcde\nfghij\nklmno"]


def test_post_discord_file_returns_false_for_missing_file() -> None:
    messages: list[str] = []

    result = discord._post_discord_file(
        "https://discord.invalid/webhook",
        {"content": "hello"},
        str(Path("missing-image.png")),
        logger=messages.append,
    )

    assert result is False
    assert messages