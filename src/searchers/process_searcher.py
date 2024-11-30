"""
Модуль, що реалізує багатопроцесний пошук ключових слів у файлах.

Надає клас ProcessSearcher для паралельного пошуку з використанням процесів.
Використовує multiprocessing.Queue для обміну даними між процесами.
"""


import multiprocessing
from typing import Dict, List, Set
from .base_searcher import BaseSearcher
from ..utils import SearchUtils


class ProcessSearcher(BaseSearcher):
    """
    Клас для багатопроцесного пошуку.
    """
    def __init__(self, keywords: Set[str], num_processes: int = 4):
        super().__init__(keywords)
        self.num_processes = num_processes

    @staticmethod
    def worker(files: List[str], keywords: Set[str], queue: multiprocessing.Queue) -> None:
        """
        Робоча функція для процесу.
        
        Args:
            files: Список файлів для обробки
            keywords: Ключові слова для пошуку
            queue: Черга для передачі результатів
        """
        local_results: Dict[str, List[str]] = {}
        for filepath in files:
            file_results = SearchUtils.search_in_file(filepath, keywords)
            for word, paths in file_results.items():
                local_results.setdefault(word, []).extend(paths)
        queue.put(local_results)

    def search(self, files: List[str]) -> Dict[str, List[str]]:
        """
        Виконує багатопроцесний пошук.
        """
        # Створюємо чергу для результатів
        queue = multiprocessing.Queue()
        processes = []

        # Розділяємо файли між процесами
        files_per_process = len(files) // self.num_processes

        # Запускаємо процеси
        for i in range(self.num_processes):
            start_idx = i * files_per_process
            end_idx = start_idx + files_per_process if i < self.num_processes - 1 else len(files)
            process_files = files[start_idx:end_idx]

            process = multiprocessing.Process(
                target=self.worker,
                args=(process_files, self.keywords, queue)
            )
            processes.append(process)
            process.start()

        # Збираємо результати
        for _ in range(self.num_processes):
            process_results = queue.get()
            for word, paths in process_results.items():
                self.results.setdefault(word, []).extend(paths)

        # Очікуємо завершення всіх процесів
        for process in processes:
            process.join()

        return self.results
