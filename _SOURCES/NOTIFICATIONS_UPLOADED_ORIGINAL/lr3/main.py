"""Демонстрация компонента message_builder: подмена стратегий канала."""
from message_builder import (
    Channel, EmailFormatter, EventType, Jinja2TemplateProvider, MessageBuilder,
    NotificationEvent, Recipient, SmsFormatter, TelegramFormatter,
)


def main() -> None:
    event = NotificationEvent(
        event_type=EventType.NEW_GRADE,
        student_name="Иванов И.И.",
        discipline="Базы данных",
        payload={"grade": "45 (отлично)"},
    )
    risk = NotificationEvent(
        event_type=EventType.RISK_GROUP,
        student_name="Петров П.П.",
        payload={"reason": "2 дисциплины не сданы"},
    )
    cases = [
        (EmailFormatter(), Recipient("s1", "Иванов", Channel.EMAIL, "ivanov@stankin.ru"), event),
        (TelegramFormatter(), Recipient("s1", "Иванов", Channel.TELEGRAM, "123456789"), event),
        (SmsFormatter(), Recipient("c1", "Куратор", Channel.SMS, "+79990000000"), risk),
    ]
    builder = MessageBuilder(Jinja2TemplateProvider(), cases[0][0])
    for formatter, recipient, ev in cases:
        builder.set_formatter(formatter)  # подмена стратегии
        msg = builder.build(ev, recipient)
        print(f"[{msg.channel.value.upper()}] to={msg.to} subject={msg.subject!r}")
        print(f"  body: {msg.body}")
        if msg.parse_mode:
            print(f"  parse_mode: {msg.parse_mode}")
        if msg.html_body:
            print(f"  html: {msg.html_body}")
        print()


if __name__ == "__main__":
    main()
