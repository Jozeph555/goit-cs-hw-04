"""
Головний модуль для запуску та тестування пошуку ключових слів у файлах.

Демонструє використання багатопотокового та багатопроцесного підходів
для пошуку ключових слів у текстових файлах.
"""


import time
from datetime import datetime
from typing import Set, Dict, List

from src.searchers import ThreadSearcher, ProcessSearcher
from src.file_handler import get_file_list, save_results_to_file


def get_user_input():
    """
    Отримання параметрів від користувача.
    """
    search_dir = input("Введіть шлях до директорії (Enter для './test_data'): ").strip()
    search_dir = search_dir or './test_data'

    keywords_input = input("Введіть ключові слова через кому: ").strip()
    keywords = (
        {word.strip() for word in keywords_input.split(',')}
        if keywords_input
        else {"Python", "programming", "test"}
    )

    threads_input = input("Введіть кількість потоків/процесів (Enter для 4): ").strip()
    num_workers = int(threads_input) if threads_input.isdigit() else 4

    return search_dir, keywords, num_workers


def search_with_threads(
    files: List[str],
    keywords: Set[str],
    num_threads: int = 4
) -> Dict[str, List[str]]:
    """
    Виконує пошук за допомогою багатопотокового підходу.
    
    Args:
        files: Список файлів для пошуку
        keywords: Ключові слова
        num_threads: Кількість потоків
        
    Returns:
        Dict[str, List[str]]: Результати пошуку
    """
    searcher = ThreadSearcher(keywords, num_threads)
    return searcher.search(files)


def search_with_processes(
    files: List[str],
    keywords: Set[str],
    num_processes: int = 4
) -> Dict[str, List[str]]:
    """
    Виконує пошук за допомогою багатопроцесного підходу.
    
    Args:
        files: Список файлів для пошуку
        keywords: Ключові слова
        num_processes: Кількість процесів
        
    Returns:
        Dict[str, List[str]]: Результати пошуку
    """
    searcher = ProcessSearcher(keywords, num_processes)
    return searcher.search(files)


def main():
    """
    Головна функція програми.
    """
    try:
        # Отримуємо параметри від користувача
        search_dir, keywords, num_workers = get_user_input()

        # Створюємо ім'я файлу для результатів з поточною датою та часом
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"search_results_{timestamp}.txt"

        files = get_file_list(search_dir)
        if not files:
            print("Не знайдено файлів для обробки!")
            return

        # Виконуємо пошук та зберігаємо час виконання
        start_time = time.time()
        thread_results = search_with_threads(files, keywords, num_workers)
        thread_time = time.time() - start_time

        start_time = time.time()
        process_results = search_with_processes(files, keywords, num_workers)
        process_time = time.time() - start_time

        # Зберігаємо результати у файл
        save_results_to_file(
            results_file,
            search_dir,
            keywords,
            num_workers,
            len(files),
            thread_results,
            process_results,
            thread_time,
            process_time
        )

        print(f"\nРезультати збережено у файл: {results_file}")

    except KeyboardInterrupt:
        print("\nПошук перервано користувачем")
    except Exception as e:
        print(f"\nПомилка при виконанні програми: {e}")


if __name__ == "__main__":
    main()
