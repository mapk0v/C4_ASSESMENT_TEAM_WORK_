# Глоссарий общих идентификаторов C4

Общие ID нужно сохранять при обновлении разных уровней C4. При создании новой диаграммы используйте эти имена для тех же логических сущностей.

| ID | Сущность | Уровень / роль |
| --- | --- | --- |
| `student` | Студент | Внешний актор |
| `teacher` | Преподаватель | Внешний актор |
| `curator` | Куратор | Внешний актор |
| `dean` | Деканат | Внешний актор |
| `assessment_system` | Информационная система аттестации | Система / системная граница |
| `mobile_app` | Мобильное приложение студента | Контейнер |
| `web_app` | Веб-приложение преподавателя и деканата | Контейнер |
| `api_gateway` | API Gateway & Backend — Markov | Контейнер |
| `analytics_service` | Analytics — Khan | Контейнер |
| `notification_service` | Notifications — Naumov | Контейнер |
| `database` | PostgreSQL | Контейнер-БД |
| `notification_gateway` | SMTP / Telegram Bot API | Внешняя система |
| `iam` | SSO/IAM | Внешняя система |
| `university_1c` | 1С:Университет | Внешняя система |
| `lms` | LMS Moodle | Внешняя система |

## Локальные идентификаторы компонентов

- Analytics: `grpc_handler`, `task_dispatcher`, `rating_calc`, `risk_detector`, `report_builder`, `analytics_repo`.
- Notifications: `grpc_handler`, `notification_router`, `message_builder`, `delivery_dispatcher`, `email_sender`, `telegram_sender`, `notification_repo`.
- Backend: `auth_mw`, `web_router`, `assessment_svc`, `rating_svc`, `report_svc`, `integration_adapter`, `repo`.

Важно: локальные имена вроде `grpc_handler` могут повторяться **в разных диаграммах отдельных контейнеров**, поскольку это разные компоненты. В единой собранной схеме потребуется уточнять их область видимости, например `analytics_grpc_handler` и `notifications_grpc_handler`. Здесь объединяется уровень контейнеров, а исходные диаграммы компонентов остаются отдельными.

## Основной межсервисный контракт

1. `api_gateway → analytics_service`: запуск аналитики по gRPC/HTTP2.
2. `analytics_service → notification_service`: события о группе риска по gRPC/HTTP2.
3. `api_gateway → notification_service`: события аттестации по gRPC/HTTP2.
4. `notification_service → notification_gateway`: отправка Email/Telegram по SMTP/HTTPS.
5. Каждый сервис читает необходимые данные из `database` по SQL/TCP 5432 согласно своим правам.

Технические контракты gRPC (protobuf, схемы DTO), фактические порты сервисов, права PostgreSQL и реализация очередей ещё должны быть согласованы при разработке реальной ИС. Эти диаграммы — **проектная архитектура**, а не доказательство работающей распределённой системы.
