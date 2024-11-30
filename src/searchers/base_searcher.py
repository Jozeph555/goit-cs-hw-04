"""
Модуль, що містить базові класи для пошуку ключових слів у файлах.

Цей модуль визначає:
- SearchUtils: утилітний клас зі спільною логікою пошуку
- BaseSearcher: абстрактний базовий клас для реалізацій пошуку
"""


from abc import ABC, abstractmethod
from typing import Dict, List, Set


class BaseSearcher(ABC):
    """
    Базовий абстрактний клас для пошуку ключових слів у файлах.
    """
    def __init__(self, keywords: Set[str]):
        self.keywords = keywords
        self.results: Dict[str, List[str]] = {}

    @abstractmethod
    def search(self, files: List[str]) -> Dict[str, List[str]]:
        """
        Абстрактний метод для реалізації пошуку.
        
        Args:
            files: Список файлів для пошуку
            
        Returns:
            Dict[str, List[str]]: Результати пошуку
        """
