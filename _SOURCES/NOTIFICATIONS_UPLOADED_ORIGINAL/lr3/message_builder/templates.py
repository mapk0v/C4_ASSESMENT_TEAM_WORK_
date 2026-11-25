"""Источник текстов уведомлений (интерфейс + реализация на Jinja2)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Mapping

from jinja2 import DictLoader, Environment, StrictUndefined

from .models import EventType


class TemplateError(Exception):
    """Шаблон для события не найден или не может быть отрисован."""


class TemplateProvider(ABC):
    """Контракт поставщика текстов (DIP: builder не знает про Jinja2)."""

    @abstractmethod
    def render(self, event_type: EventType, context: Mapping[str, str]) -> str:
        """Вернуть нейтральный (без разметки канала) текст уведомления."""


DEFAULT_TEMPLATES: dict[str, str] = {
    EventType.NEW_GRADE.value: (
        "{{ student_name }}, по дисциплине «{{ discipline }}» "
        "выставлена оценка: {{ grade }}."
    ),
    EventType.RISK_GROUP.value: (
        "{{ student_name }}, вы попали в группу риска по успеваемости. "
        "Причина: {{ reason }}. Обратитесь к куратору."
    ),
    EventType.RATING_CHANGED.value: (
        "{{ student_name }}, ваш рейтинг изменился: "
        "{{ old_rank }} → {{ new_rank }}."
    ),
}


class Jinja2TemplateProvider(TemplateProvider):
    """Отрисовка шаблонов Jinja2; отсутствующая переменная — ошибка."""

    def __init__(self, templates: Mapping[str, str] | None = None) -> None:
        source = dict(templates) if templates is not None else DEFAULT_TEMPLATES
        self._env = Environment(
            loader=DictLoader(source), undefined=StrictUndefined, autoescape=False
        )

    def render(self, event_type: EventType, context: Mapping[str, str]) -> str:
        try:
            template = self._env.get_template(event_type.value)
            return str(template.render(**context))
        except Exception as exc:  # TemplateNotFound, UndefinedError и т.п.
            raise TemplateError(f"{event_type.value}: {exc}") from exc
