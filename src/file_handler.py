"""
Модуль для роботи з файлами.

Надає функції для:
- читання вмісту файлів
- отримання списку файлів з директорії
"""


from pathlib import Path
from typing import Dict, List, Optional


def read_file(filepath: str, encoding: str = 'utf-8') -> Optional[str]:
    """
    Читає вміст файлу з обробкою помилок.
    
    Args:
        filepath: Шлях до файлу
        encoding: Кодування файлу (за замовчуванням utf-8)
        
    Returns:
        Optional[str]: Вміст файлу або None у випадку помилки
        
    Raises:
        FileNotFoundError: Якщо файл не знайдено
        PermissionError: Якщо немає прав доступу до файлу
        UnicodeDecodeError: Якщо виникла помилка декодування
    """
    path = Path(filepath)
    try:
        return path.read_text(encoding=encoding)
    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
    except PermissionError:
        print(f"Відмовлено у доступі до файлу: {path}")
    except UnicodeDecodeError:
        print(f"Помилка декодування файлу: {path}")
    except Exception as e:
        print(f"Неочікувана помилка при читанні файлу {path}: {e}")
    return None


def get_file_list(directory: str, extensions: set = None) -> List[str]:
    """
    Рекурсивно отримує список файлів у директорії.
    
    Args:
        directory: Шлях до директорії
        extensions: Набір розширень для фільтрації (якщо None, використовуються 
                    стандартні текстові розширення)
        
    Returns:
        List[str]: Список абсолютних шляхів до файлів
        
    Raises:
        FileNotFoundError: Якщо директорію не знайдено
        PermissionError: Якщо немає прав доступу до директорії
    """
    if extensions is None:
        extensions = {'.txt', '.csv', '.md', '.log', '.json', '.xml', '.yml', '.yaml'}

    file_list = []

    try:
        path = Path(directory)

        if not path.exists():
            raise FileNotFoundError(f"Директорію не знайдено: {directory}")

        if not path.is_dir():
            raise NotADirectoryError(f"Вказаний шлях не є директорією: {directory}")

        for element in path.iterdir():
            if element.is_dir():
                # Рекурсивно додаємо файли з піддиректорій
                file_list.extend(get_file_list(str(element), extensions))
            elif element.is_file() and element.suffix.lower() in extensions:
                # Додаємо абсолютний шлях до файлу
                file_list.append(str(element.absolute()))

        return sorted(file_list)  # Сортуємо для консистентності

    except PermissionError:
        print(f"Відмовлено у доступі до директорії: {directory}")
        return []
    except Exception as e:
        print(f"Помилка при отриманні списку файлів: {e}")
        return []


def save_results_to_file(
    filename: str,
    search_dir: str,
    keywords: set,
    num_workers: int,
    files_count: int,
    thread_results: dict,
    process_results: dict,
    thread_time: float,
    process_time: float
) -> None:
    """
    Зберігає результати пошуку у текстовий файл.
    
    Args:
        filename: Ім'я файлу для збереження результатів
        search_dir: Директорія пошуку
        keywords: Ключові слова
        num_workers: Кількість потоків/процесів
        files_count: Кількість оброблених файлів
        thread_results: Результати пошуку в потоках
        process_results: Результати пошуку в процесах
        thread_time: Час виконання пошуку в потоках
        process_time: Час виконання пошуку в процесах
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Записуємо параметри пошуку
        f.write("Параметри пошуку:\n")
        f.write(f"- Директорія: {search_dir}\n")
        f.write(f"- Ключові слова: {', '.join(keywords)}\n")
        f.write(f"- Кількість потоків/процесів: {num_workers}\n")
        f.write(f"\nЗнайдено {files_count} файлів для обробки\n")

        # Записуємо результати та час виконання для потоків
        f.write("\nРезультати пошуку (потоки):\n")
        f.write("=" * 50 + "\n")
        f.write(f"Час виконання: {thread_time:.4f} секунд\n")  # Додано
        write_search_results(f, thread_results)

        # Записуємо результати та час виконання для процесів
        f.write("\nРезультати пошуку (процеси):\n")
        f.write("=" * 50 + "\n")
        f.write(f"Час виконання: {process_time:.4f} секунд\n")  # Додано
        write_search_results(f, process_results)

        # Порівняння часу виконання
        f.write("\nПорівняння часу виконання:\n")  # Додано
        f.write("-" * 50 + "\n")  # Додано
        f.write(f"- Потоки:   {thread_time:.4f} секунд\n")  # Додано
        f.write(f"- Процеси:  {process_time:.4f} секунд\n")  # Додано
        f.write(f"- Різниця:  {abs(thread_time - process_time):.4f} секунд\n")  # Додано


def write_search_results(f, results: dict) -> None:
    """
    Записує результати пошуку у файл.
    
    Args:
        f: Файловий об'єкт для запису
        results: Результати пошуку
    """
    for keyword, files in results.items():
        f.write(f"\nКлючове слово '{keyword}':\n")
        f.write(f"- Знайдено у {len(files)} файлах:\n")
        for file in files:
            f.write(f"  • {file}\n")

    # Записуємо загальну статистику
    total_files = len({file for files in results.values() for file in files})
    f.write("\nЗагальна статистика:\n")
    f.write("-" * 50 + "\n")
    f.write(f"Всього унікальних файлів: {total_files}\n")
    f.write(f"Всього ключових слів: {len(results)}\n")

    # Записуємо частоту знаходження
    f.write("\nЧастота знаходження слів:\n")
    for word, files in sorted(results.items(), key=lambda x: len(x[1]), reverse=True):
        f.write(f"- '{word}': {len(files)} файл(ів)\n")


def count_keyword_occurrences(results: Dict[str, List[str]]) -> Dict[str, int]:
    """
    Підраховує кількість знаходжень кожного ключового слова.
    
    Args:
        results: Словник результатів пошуку, де ключ - слово, 
                значення - список файлів
                
    Returns:
        Dict[str, int]: Словник, де ключ - слово, 
                        значення - кількість файлів, де знайдено слово
    """
    return {word: len(files) for word, files in results.items()}
