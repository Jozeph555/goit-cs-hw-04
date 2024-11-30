# Keyword Search System

Навчальна програма для паралельного пошуку ключових слів у текстових файлах. 
Реалізує та порівнює багатопотоковий та багатопроцесний підходи до пошуку.

## Опис програми

Програма дозволяє:
- Виконувати пошук заданих ключових слів у текстових файлах
- Порівнювати ефективність багатопотокового та багатопроцесного підходів
- Зберігати результати пошуку у текстовий файл
- Отримувати статистику по знайдених словах

## Структура проєкту

```plaintext
goit-cs-hw-04/
│
├── src/
│   ├── init.py
│   ├── file_handler.py      # Функції для роботи з файлами
│   ├── searchers/
│   │   ├── init.py
│   │   ├── base_searcher.py # Базовий клас для пошуку
│   │   ├── thread_searcher.py
│   │   └── process_searcher.py
│   └── utils.py            # Допоміжні функції
│
├── main.py
├── requirements.txt
├── README.md
└── search_results_20241129_223211.txt  # Приклад файлу з результатами

## Встановлення

1. Клонувати репозиторій:

```bash
git clone <repository-url>
cd goit-cs-hw-04

2. Створити та активувати віртуальне середовище:

```bash
python -m venv .venv
source .venv/bin/activate  # для macOS/Linux

## Використання

1. Запустити програму:

```bash
python main.py

2. Ввести параметри пошуку:

* Шлях до директорії (або Enter для використання './test_data')
* Ключові слова через кому
* Кількість потоків/процесів (або Enter для використання 4)

3. Результати будуть збережені у файл search_results_YYYYMMDD_HHMMSS.txt

## Формат результатів
Файл з результатами містить:

* Параметри пошуку
* Результати пошуку для кожного методу
* Статистику знаходження ключових слів
* Порівняння часу виконання методів
* Інформацію про розбіжності у результатах (якщо є)

## Особливості реалізації

* Використання абстрактного базового класу для пошуку
* Паралельна обробка файлів
* Вимірювання часу виконання
* Обробка помилок декодування файлів
* Порівняння ефективності різних підходів