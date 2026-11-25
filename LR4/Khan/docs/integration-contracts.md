# Интерфейсы Analytics для общей диаграммы тимлида

## 1. Глобальные ID

| ID | Объект |
| --- | --- |
| `assessment_system` | ИС аттестации (система) |
| `api_gateway` | Backend (контейнер) |
| `analytics_service` | Analytics (контейнер) |
| `notification_service` | Notifications (контейнер) |
| `database` | PostgreSQL (контейнер) |
| `grpc_handler` | Приём gRPC внутри Analytics |
| `analytics_coordinator` | Координатор сценариев Analytics |
| `analytics_repo` | Доступ к аналитическим данным |
| `rating_calc` | Калькулятор аналитических показателей L3/L4 |
| `risk_detector` | Детектор групп риска, **не вызывается** в выбранном Dynamic-сценарии |

## 2. Сквозной сценарий «Расчёт показателя за первый модуль»

| № | Откуда → куда | Данные / операция | Протокол |
| --- | --- | --- | --- |
| 1 | student → mobile_app | Выбор первого модуля | UI |
| 2 | mobile_app → api_gateway | Студент, учебный год, номер модуля | HTTPS/JSON |
| 3 | api_gateway → grpc_handler | `CalculateRating(student_id, year, module=1, strategy)` | gRPC/HTTP2 |
| 4 | grpc_handler → analytics_coordinator | Валидированные аргументы | in-process |
| 5 | analytics_coordinator → analytics_repo | `get_module_grades(...)` | Python Call |
| 6 | analytics_repo → database | SELECT для выбранного модуля | SQL/TCP 5432 |
| 7 | database → analytics_repo | Строки результатов аттестации | SQL result |
| 8 | analytics_repo → analytics_coordinator | `list[ModuleGrade]` | in-process |
| 9 | analytics_coordinator → rating_calc | `calculate_rating(student, year, module, grades)` | Python Call |
| 10 | rating_calc → analytics_coordinator | `RatingSummary` | in-process |
| 11 | analytics_coordinator → grpc_handler | Рассчитанный показатель, число несданных | in-process |
| 12 | grpc_handler → api_gateway | `CalculateRatingResponse` | gRPC/HTTP2 |
| 13 | api_gateway → mobile_app | Показатель за первый модуль | HTTPS/JSON |

Имена gRPC-операций и полей — **проектные соглашения**, поскольку реальные `.proto` ещё не разрабатывались. Допускается согласовать имена с Backend до объединения.

## 3. Внутренняя граница

В ЛР3 `RatingCalculator.calculate_rating` получает массив баллов по дисциплинам. В сценарии ЛР4 этот массив передаёт `analytics_coordinator`, а не БД напрямую. Поэтому `rating_calc` остаётся независим от SQL, gRPC и Docker. Оценки модулей не объединяются.

## 4. Для защиты

Студент объясняет порядок вызовов, зачем нужны gRPC и SQL, как выбранный модуль передаётся через все слои и почему `rating_calc` не обращается напрямую в PostgreSQL.
