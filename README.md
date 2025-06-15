## Задание №1 из ТЗ VK Predict. Исполнитель: В. Гильмутдинов

Проект для генерации push-уведомлений через OpenAI API.

## Структура

.env.example

segments.json

main.py

README.md



## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <repo_url>
   cd push-notifier
Установите зависимости:

pip install python-dotenv openai

## Вставьте ваш OPENAI_API_KEY в .env

Скопируйте .env и вставьте ключ:

## Использование

Отредактируйте segments.json, если нужно добавить новые имена, сегменты или сроки.

Запустите генерацию: python main.py

В консоли появятся 5 вариантов push-уведомлений.

