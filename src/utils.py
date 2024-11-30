"""
клас з методами для пошуку ключових слів у файлах.
"""


from typing import Dict, List, Set
from .file_handler import read_file


class SearchUtils:
    """
    Утилітний клас для спільної логіки пошуку
    """
    @staticmethod
    def search_in_file(filepath: str, keywords: Set[str]) -> Dict[str, List[str]]:
        """
        Пошук ключових слів в окремому файлі.
        
        Args:
            filepath: Шлях до файлу
            keywords: Набір ключових слів
            
        Returns:
            Dict[str, List[str]]: Словник знайдених слів та їх розташування
        """
        content = read_file(filepath)
        if content is not None:  # Перевіряємо, чи вдалося прочитати файл
            local_results = {}
            content = content.lower()
            for word in keywords:
                if word.lower() in content:
                    local_results.setdefault(word, []).append(filepath)
            return local_results
        return {}
