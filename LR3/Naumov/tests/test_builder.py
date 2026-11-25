import pytest

from message_builder import (
    Channel, ChannelMismatchError, EmailFormatter, EventType,
    Jinja2TemplateProvider, MessageBuilder, NotificationEvent, Recipient,
    SmsFormatter, TelegramFormatter, TemplateError,
)

EVENT = NotificationEvent(
    EventType.NEW_GRADE, "Иванов И.И.", "1-й модуль", "Базы данных", {"grade": "45"}
)


def rcpt(channel: Channel, address: str = "x") -> Recipient:
    return Recipient("r1", "Имя", channel, address)


@pytest.fixture
def builder() -> MessageBuilder:
    return MessageBuilder(Jinja2TemplateProvider(), EmailFormatter())


def test_email_has_subject_and_html(builder: MessageBuilder) -> None:
    msg = builder.build(EVENT, rcpt(Channel.EMAIL, "a@b.ru"))
    assert msg.subject == "Новая оценка"
    assert msg.to == "a@b.ru"
    assert msg.html_body is not None and "<p>" in msg.html_body
    assert "Базы данных" in msg.body


def test_email_html_is_escaped(builder: MessageBuilder) -> None:
    ev = NotificationEvent(EventType.NEW_GRADE, "<b>X</b>", "1-й модуль", "БД", {"grade": "45"})
    msg = builder.build(ev, rcpt(Channel.EMAIL))
    assert msg.html_body is not None and "&lt;b&gt;" in msg.html_body


def test_telegram_escapes_markdown(builder: MessageBuilder) -> None:
    builder.set_formatter(TelegramFormatter())
    msg = builder.build(EVENT, rcpt(Channel.TELEGRAM))
    assert msg.parse_mode == "MarkdownV2"
    assert "Иванов И\\.И\\." in msg.body


def test_telegram_limit() -> None:
    long_event = NotificationEvent(
        EventType.NEW_GRADE, "а" * 5000, "1-й модуль", "БД", {"grade": "45"}
    )
    b = MessageBuilder(Jinja2TemplateProvider(), TelegramFormatter())
    msg = b.build(long_event, rcpt(Channel.TELEGRAM))
    assert len(msg.body) <= TelegramFormatter.MAX_LENGTH


def test_telegram_text_part_not_over_limit() -> None:
    fmt = TelegramFormatter()
    fitted = fmt._fit("." * 5000)
    assert len(fitted) <= TelegramFormatter.MAX_LENGTH
    assert not fitted.rstrip("…").endswith("\\")


def test_sms_truncated() -> None:
    ev = NotificationEvent(EventType.NEW_GRADE, "я" * 400, "1-й модуль", "БД", {"grade": "45"})
    b = MessageBuilder(Jinja2TemplateProvider(), SmsFormatter())
    msg = b.build(ev, rcpt(Channel.SMS))
    assert len(msg.body) == SmsFormatter.MAX_LENGTH and msg.body.endswith("…")


def test_strategy_swap_changes_output(builder: MessageBuilder) -> None:
    first = builder.build(EVENT, rcpt(Channel.EMAIL))
    builder.set_formatter(TelegramFormatter())
    second = builder.build(EVENT, rcpt(Channel.TELEGRAM))
    assert first.channel is Channel.EMAIL and second.channel is Channel.TELEGRAM


def test_channel_mismatch(builder: MessageBuilder) -> None:
    with pytest.raises(ChannelMismatchError):
        builder.build(EVENT, rcpt(Channel.TELEGRAM))


def test_missing_variable_raises() -> None:
    ev = NotificationEvent(EventType.RISK_GROUP, "Петров", "1-й модуль")  # нет reason
    b = MessageBuilder(Jinja2TemplateProvider(), EmailFormatter())
    with pytest.raises(TemplateError):
        b.build(ev, rcpt(Channel.EMAIL))


def test_custom_template_provider() -> None:
    from message_builder import TemplateProvider

    class Fake(TemplateProvider):
        def render(self, event_type, context):  # type: ignore[no-untyped-def]
            return "fake"

    msg = MessageBuilder(Fake(), EmailFormatter()).build(EVENT, rcpt(Channel.EMAIL))
    assert msg.body == "fake"


@pytest.mark.parametrize("points", [0, 24, 25, 34, 35, 44, 45, 54])
def test_54_point_boundaries_are_valid(points: int) -> None:
    ev = NotificationEvent(EventType.NEW_GRADE, "Иванов", "2-й модуль", "БД", {"grade": str(points)})
    msg = MessageBuilder(Jinja2TemplateProvider(), EmailFormatter()).build(ev, rcpt(Channel.EMAIL))
    assert f"{points} из 54" in msg.body
    assert "2-й модуль" in msg.body


@pytest.mark.parametrize("points", ["-1", "55", "5.0", "отлично", ""])
def test_out_of_range_or_wrong_format_is_rejected(points: str) -> None:
    with pytest.raises(ValueError, match="от 0 до 54"):
        NotificationEvent(EventType.NEW_GRADE, "Иванов", "1-й модуль", "БД", {"grade": points})


def test_module_is_required() -> None:
    with pytest.raises(ValueError, match="модуль"):
        NotificationEvent(EventType.RISK_GROUP, "Иванов", "", payload={"reason": "низкий балл"})


def test_two_modules_do_not_get_mixed(builder: MessageBuilder) -> None:
    first = builder.build(EVENT, rcpt(Channel.EMAIL))
    second = builder.build(
        NotificationEvent(EventType.NEW_GRADE, "Иванов И.И.", "2-й модуль", "Базы данных", {"grade": "33"}),
        rcpt(Channel.EMAIL),
    )
    assert "1-й модуль" in first.body and "45 из 54" in first.body
    assert "2-й модуль" in second.body and "33 из 54" in second.body


def test_risk_message_is_appropriate_for_curator(builder: MessageBuilder) -> None:
    ev = NotificationEvent(EventType.RISK_GROUP, "Петров П.П.", "2-й модуль", payload={"reason": "два долга"})
    msg = builder.build(ev, Recipient("curator1", "Куратор", Channel.EMAIL, "curator@stankin.ru"))
    assert "Куратор" in msg.body and "Петров" in msg.body


def test_event_payload_cannot_override_identity(builder: MessageBuilder) -> None:
    event = NotificationEvent(
        EventType.NEW_GRADE, "Иванов", "1-й модуль", "БД",
        {"grade": "42", "student_name": "Чужой", "module": "неверный"},
    )
    msg = builder.build(event, rcpt(Channel.EMAIL))
    assert "Иванов" in msg.body and "Чужой" not in msg.body
