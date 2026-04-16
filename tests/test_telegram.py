from notify_bridge import telegram


def test_chat_id_matches_plain_and_supergroup_variants() -> None:
    assert telegram.chat_id_matches("-5216326159", -1005216326159)
    assert telegram.chat_id_matches("-1005216326159", "-1005216326159")
    assert not telegram.chat_id_matches("123", "456")


def test_extract_update_text_reads_message_text() -> None:
    text, message = telegram.extract_update_text({"message": {"text": "  hello  "}})

    assert text == "hello"
    assert message == {"text": "  hello  "}


def test_split_text_prefers_newline_boundaries() -> None:
    chunks = telegram._split_text("first\nsecond\nthird", limit=8)

    assert chunks == ["first", "second", "third"]


def test_split_text_falls_back_to_hard_limit() -> None:
    chunks = telegram._split_text("abcdefghij", limit=4)

    assert chunks == ["abcd", "efgh", "ij"]