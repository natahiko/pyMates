"""Модулі з командами. Імпорт модуля реєструє його команди в ``COMMANDS``.

Новий модуль (наприклад, ``notes``) достатньо додати в імпорт нижче.
Порядок імпорту = порядок розділів у ``help``.
"""

from . import general  # noqa: F401  (має йти першим)
from . import contacts  # noqa: F401
from . import notes  # noqa: F401

__all__ = ["general", "contacts", "notes"]
