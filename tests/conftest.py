"""Спільні фікстури тестів; pytest підхоплює їх у всіх файлах автоматично."""

import pytest

from personal_assistant.cli import prompts
from personal_assistant.context import AppContext
from personal_assistant.models import AddressBook, NoteBook


@pytest.fixture(autouse=True)
def no_colors(monkeypatch):
    """Вимкнути кольори, щоб тести однаково працювали в терміналі й у PyCharm."""
    monkeypatch.setenv("NO_COLOR", "1")


@pytest.fixture
def ctx():
    """Порожній контекст застосунку (дані лише в пам'яті, не на диску)."""
    return AppContext(book=AddressBook(), notes=NoteBook())


@pytest.fixture
def answers(monkeypatch):
    """Черга відповідей, які отримають діалоги замість клавіатури.

    Додайте відповіді до виклику команди: ``answers += ["John", ""]``.
    Якщо команда спитає більше, ніж є в черзі, тест упаде з назвою питання.
    """
    queue: list[str] = []

    def fake_input(prompt):
        """Повернути наступну відповідь з черги."""
        if not queue:
            raise AssertionError(f"Unexpected prompt: {prompt}")
        return queue.pop(0)

    monkeypatch.setattr(prompts, "input_func", fake_input)
    return queue
