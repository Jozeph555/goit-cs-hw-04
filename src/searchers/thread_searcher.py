"""
Модуль, що реалізує багатопотоковий пошук ключових слів у файлах.

Надає клас ThreadSearcher для паралельного пошуку з використанням потоків.
Підтримує синхронізований доступ до спільних ресурсів через threading.Lock.
"""


import threading
from typing import Dict, List, Set
from .base_searcher import BaseSearcher
from ..utils import SearchUtils


class ThreadSearcher(BaseSearcher):
    """
    Клас для багатопотокового пошуку.
    """
    def __init__(self, keywords: Set[str], num_threads: int = 4):
        super().__init__(keywords)
        self.num_threads = num_threads
        self.lock = threading.Lock()

    def worker(self, files: List[str]) -> None:
        """
        Робоча функція для потоку.
        """
        for filepath in files:
            local_results = SearchUtils.search_in_file(filepath, self.keywords)
            with self.lock:
                for word, paths in local_results.items():
                    self.results.setdefault(word, []).extend(paths)

    def search(self, files: List[str]) -> Dict[str, List[str]]:
        """
        Виконує багатопотоковий пошук.
        """
        # Розділяємо файли між потоками
        files_per_thread = len(files) // self.num_threads
        threads = []

        for i in range(self.num_threads):
            start_idx = i * files_per_thread
            end_idx = start_idx + files_per_thread if i < self.num_threads - 1 else len(files)
            thread_files = files[start_idx:end_idx]

            thread = threading.Thread(target=self.worker, args=(thread_files,))
            threads.append(thread)
            thread.start()

        # Очікуємо завершення всіх потоків
        for thread in threads:
            thread.join()

        return self.results
