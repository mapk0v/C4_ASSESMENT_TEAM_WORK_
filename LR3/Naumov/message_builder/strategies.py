"""Стратегии форматирования сообщения под канал (паттерн Strategy)."""
from __future__ import annotations

import html
import re
from abc import ABC, abstractmethod

from .models import Channel, EventType, Message, NotificationEvent, Recipient


class ChannelFormatter(ABC):
    """Интерфейс стратегии: один контракт, разные алгоритмы форматирования."""

    @property
    @abstractmethod
    def channel(self) -> Channel:
        """Канал, который обслуживает стратегия."""

    @abstractmethod
    def format(
        self, text: str, event: NotificationEvent, recipient: Recipient
    ) -> Message:
        """Превратить нейтральный текст в сообщение формата канала."""


_EMAIL_SUBJECTS: dict[EventType, str] = {
    EventType.NEW_GRADE: "Новая оценка",
    EventType.RISK_GROUP: "Внимание: группа риска",
    EventType.RATING_CHANGED: "Изменение рейтинга",
}


class EmailFormatter(ChannelFormatter):
    """Тема письма + plain и HTML-версии тела."""

    @property
    def channel(self) -> Channel:
        return Channel.EMAIL

    def format(
        self, text: str, event: NotificationEvent, recipient: Recipient
    ) -> Message:
        subject = _EMAIL_SUBJECTS[event.event_type]
        safe = html.escape(text)
        html_body = f"<html><body><h3>{subject}</h3><p>{safe}</p></body></html>"
        return Message(
            channel=Channel.EMAIL,
            to=recipient.address,
            subject=subject,
            body=text,
            html_body=html_body,
        )


class TelegramFormatter(ChannelFormatter):
    """MarkdownV2: экранирование спецсимволов и лимит 4096 символов."""

    MAX_LENGTH: int = 4096
    _SPECIAL = re.compile(r"([_*\[\]()~`>#+\-=|{}.!\\])")

    @property
    def channel(self) -> Channel:
        return Channel.TELEGRAM

    def _escape(self, text: str) -> str:
        return self._SPECIAL.sub(r"\\\1", text)

    def _fit(self, text: str, limit: int | None = None) -> str:
        """Экранировать и обрезать, не разрывая escape-последовательность."""
        max_len = self.MAX_LENGTH if limit is None else max(0, limit)
        out: list[str] = []
        size = 0
        for char in text:
            piece = self._escape(char)
            if size + len(piece) > max_len:
                if size < max_len:
                    out.append("…")
                break
            out.append(piece)
            size += len(piece)
        return "".join(out)

    def format(
        self, text: str, event: NotificationEvent, recipient: Recipient
    ) -> Message:
        title = _EMAIL_SUBJECTS[event.event_type]
        prefix = f"*{self._escape(title)}*\n"
        body = prefix + self._fit(text, self.MAX_LENGTH - len(prefix))
        return Message(
            channel=Channel.TELEGRAM,
            to=recipient.address,
            body=body,
            parse_mode="MarkdownV2",
        )


class SmsFormatter(ChannelFormatter):
    """Расширение без правки builder'а: короткий текст до 160 символов."""

    MAX_LENGTH: int = 160

    @property
    def channel(self) -> Channel:
        return Channel.SMS

    def format(
        self, text: str, event: NotificationEvent, recipient: Recipient
    ) -> Message:
        flat = " ".join(text.split())
        if len(flat) > self.MAX_LENGTH:
            flat = flat[: self.MAX_LENGTH - 1] + "…"
        return Message(channel=Channel.SMS, to=recipient.address, body=flat)
