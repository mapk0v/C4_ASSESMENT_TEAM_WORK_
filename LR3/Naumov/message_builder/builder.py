"""MessageBuilder — контекст паттерна Strategy (компонент message_builder)."""
from __future__ import annotations

from .models import Message, NotificationEvent, Recipient
from .strategies import ChannelFormatter
from .templates import TemplateProvider


class ChannelMismatchError(ValueError):
    """Канал получателя не совпадает с каналом текущей стратегии."""


class MessageBuilder:
    """Формирует сообщение: шаблон -> стратегия форматирования канала."""

    def __init__(self, templates: TemplateProvider, formatter: ChannelFormatter) -> None:
        self._templates: TemplateProvider = templates
        self._formatter: ChannelFormatter = formatter

    def set_formatter(self, formatter: ChannelFormatter) -> None:
        """Подмена стратегии во время работы (без правки этого класса)."""
        self._formatter = formatter

    def build(self, event: NotificationEvent, recipient: Recipient) -> Message:
        if recipient.channel is not self._formatter.channel:
            raise ChannelMismatchError(
                f"получатель {recipient.recipient_id}: {recipient.channel.value}, "
                f"стратегия: {self._formatter.channel.value}"
            )
        context = {
            **event.payload,
            "student_name": event.student_name,
            "discipline": event.discipline,
            "module": event.module,
            "recipient_name": recipient.name,
        }
        text = self._templates.render(event.event_type, context)
        return self._formatter.format(text, event, recipient)
