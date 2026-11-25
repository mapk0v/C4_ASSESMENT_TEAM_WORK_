# ИСИТ — материалы по лабораторным и участникам

Структура сформирована по лабораторным работам **LR1 → LR2 → LR3 → LR4**, затем по участникам **Khan, Markov, Naumov**. Это удобное распределение ответственности; оно **не всегда совпадает с автором конкретного Git-коммита**.

## Где чьи файлы

| Папка | Ответственный раздел | Что внутри |
| --- | --- | --- |
| `LR1/General/` | Общая работа группы | Контекстная диаграмма и диаграмма контейнеров |
| `LR2/Khan/` | Khan — Analytics / SAaR | Его компонентная диаграмма |
| `LR2/Markov/` | Markov — Backend | Компонентная диаграмма Backend (в Git файл добавлял аккаунт `kirrusshka`) |
| `LR2/Naumov/` | Naumov — Notifications | Компонентная диаграмма уведомлений |
| `LR3/Khan/` | Khan — Analytics / `rating_calc` | Личный прототип ЛР3: Python-код, UML классов, 15 тестов, описание, отчёт и инструкция по интеграции |
| `LR3/Markov/` | Markov — `rating_service` | Python-прототип и UML из GitHub |
| `LR3/Naumov/` | Naumov — `message_builder` | Исправленная ЛР3 по уведомлениям: Python, тесты, UML и PNG |
| `LR4/Khan/` | Khan — Analytics | Диаграммы L0/Dynamic/Deployment, дополнительные документы и отчёт |
| `LR4/Markov/` | Markov — Backend | Три оригинальные диаграммы L0/Dynamics/Deployment из GitHub |
| `LR4/Naumov/` | Naumov — Notifications | Три проверенные диаграммы и PNG |

`LR4/vendor/` — C4-PlantUML: нужна для локального рендера диаграмм `LR4/Naumov/*.puml`. Не удалять.

## Где оригиналы

- `_SOURCES/GITHUB_ORIGINAL_MAIN/` — **полный неизменённый снимок всех 15 отслеживаемых файлов** GitHub на коммите `c5f75ebffeed4f75157ad534c7baecee4fbc610e`. Присутствует `rating_service/.gitignore`.
- `_SOURCES/NOTIFICATIONS_UPLOADED_ORIGINAL/` — содержимое присланного пользователем архива по уведомлениям **без исправлений**.
- `LR3/Khan/` — **все 11 файлов из присланного архива** `LR3_Analytics_STANKIN_complete(1).zip`; пользователь обозначил их как свою ЛР3. Содержимое исходников не изменялось.
- `_INTEGRATION_PROPOSALS/` — предлагаемые исправления общих файлов команды. **Не были опубликованы в GitHub** и не должны восприниматься как исходные работы участников.

## История и проверка авторства

Подробности — `OWNERSHIP.md` и `OWNERSHIP.csv` (Git-авторы по каждому исходному файлу). Имена участников распределены по направлению работы:

- **Khan** — Analytics (в Git `kirrusshka`).
- **Markov** — Backend и его `rating_service` (в Git `mapkov` / `mark0v`).
- **Naumov** — Notifications (в Git `Sashka`).

Это сопоставление имеет учебный характер: в частности, общую компонентную диаграмму Backend загрузил `kirrusshka`, хотя она помещена в каталог `LR2/Markov` по специализации сервиса.

## Проверка ЛР3 Khan

В `LR3/Khan/` теперь находится собственный 54-балльный прототип Analytics. Команда `python -m unittest discover -s tests -v` успешно выполняет 15 тестов, `python main.py` запускает демонстрацию, UML `class_diagram.puml` проходит синтаксическую проверку PlantUML. Рейтинговый прототип Маркова оставлен отдельно в `LR3/Markov`, чтобы не перепутать авторов и реализации.
