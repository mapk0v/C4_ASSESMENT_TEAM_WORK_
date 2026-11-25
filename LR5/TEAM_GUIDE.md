# ЛР5 — интеграция команды и порядок защиты

## Что подготовлено

- Общая структура `LR1`–`LR4` по участникам.
- Сводная C4-диаграмма `src/main.puml`.
- Скрипт `scripts/render-diagrams.sh` и GitHub Actions `render-docs.yml`.
- Единые ID в `GLOSSARY_IDS.md` и исправленные межсервисные связи.
- Локально проверены **22 PlantUML-диаграммы**, сгенерированы **22 PNG и 22 SVG**. Это результат локальной сборки, а не логи GitHub Actions.
- Тесты Python: Analytics Khan — **15 успешно**; Notifications Naumov — **27 успешно**. Демонстрация Backend Markov запускается, но использует старую шкалу оценивания (подробности `KNOWN_ISSUES.md`).

## Тимлид

1. Скопировать **содержимое** архива в корень репозитория. Важно: не класть всю папку `LR5_ISIT_TEAM_REPO_READY` внутрь текущего репозитория — тогда путь `.github/workflows` окажется неправильным.
   **Перед копированием** сопоставить прежние корневые диаграммы с новыми файлами `LR1`–`LR4`, чтобы не оставить разные активные версии одних и тех же диаграмм. Старые файлы не удалять без проверки (`KNOWN_ISSUES.md`).
2. Убедиться, что в GitHub есть `.github/workflows/render-docs.yml`.
3. Проверить `Settings → Branches → Branch protection rules` / rulesets: требовать PR, review и успешную проверку `Validate PlantUML and build PNG/SVG` для `main` (если тариф и права репозитория позволяют).
4. Проверить PR каждого участника, согласование ID, протоколов и входящих/исходящих стрелок.
5. Выполнить merge одобренных PR. Проверить зелёный статус CI и скачать артефакт.

## Каждый разработчик

1. Настроить Git, VS Code, расширение PlantUML. При необходимости использовать локальный Docker PlantUML Server по методичке.
2. Создать ветку, например `feature/khan-lr5-analytics`.
3. Изменить свои файлы диаграмм и проверить их с помощью скрипта из корня проекта.
4. Зафиксировать изменения (`git add`, `git commit`) и отправить ветку (`git push -u origin feature/khan-lr5-analytics`).
5. На GitHub открыть Pull Request в `main` и дождаться статуса CI.
6. При ошибке открыть `Actions`, прочитать лог шага `Validate and render C4 diagrams`, исправить файл и отправить новый commit.
7. Отправить преподавателю скриншоты PR, успеха CI, лога проверки и готовой диаграммы.

## Пример команд для Khan

```bash
git switch -c feature/khan-lr5-analytics
bash scripts/render-diagrams.sh /absolute/path/to/plantuml.jar
git add LR2/Khan LR3/Khan LR4/Khan LR5/Khan
git commit -m "docs: integrate Analytics C4 diagrams for LR5"
git push -u origin feature/khan-lr5-analytics
```

Условие: скрипт, библиотека и workflow должны предварительно находиться в ветке проекта. Если тимлид сначала подготовит инфраструктуру в отдельном PR, у каждого участника после обновления ветки будут те же средства проверки.

## Скриншоты для защиты (сделать после загрузки на GitHub)

1. Структура `LR1`–`LR5` и `.github/workflows/render-docs.yml`.
2. Открытый PR `feature/khan-lr5-analytics → main`.
3. Зелёная галочка `Validate PlantUML and build PNG/SVG`.
4. Лог с `SUCCESS: validated ... diagrams; generated ... PNG and ... SVG files`.
5. Содержимое артефакта `c4-architecture-diagrams` и сводная диаграмма `src/main.png`.

**Не изображать локальные логи как результаты GitHub Actions.** После запуска онлайн нужно вставить реальные скриншоты.
