"""Доменные модели компонента message_builder (L4)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Mapping


class Channel(str, Enum):
    """Канал доставки уведомления."""

    EMAIL = "email"
    TELEGRAM = "telegram"
    SMS = "sms"


class EventType(str, Enum):
    """Тип события, инициирующего уведомление (приходит от grpc_handler)."""

    NEW_GRADE = "new_grade"
    RISK_GROUP = "risk_group"
    RATING_CHANGED = "rating_changed"


@dataclass(frozen=True)
class NotificationEvent:
    """Валидированное событие, переданное notification_router."""

    event_type: EventType
    student_name: str
    discipline: str = ""
    payload: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Recipient:
    """Получатель: адрес зависит от канала (email, chat_id, телефон)."""

    recipient_id: str
    name: str
    channel: Channel
    address: str


@dataclass(frozen=True)
class Message:
    """Готовое к отправке сообщение для email_sender / telegram_sender."""

    channel: Channel
    to: str
    body: str
    subject: str | None = None
    html_body: str | None = None
    parse_mode: str | None = None
