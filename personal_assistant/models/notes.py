"""Нотатки: окрема сутність, не пов'язана з адресною книгою.

``Note`` - одна нотатка (ID, текст, дата створення).
``NoteBook`` - колекція нотаток, ключ - ID. Редагування й видалення
відбуваються за ID.
"""

from collections import UserDict
from datetime import datetime

from .tags import add_tags as add_tags_to_list
from .tags import has_tag
from .tags import has_tag, tag_sort_key

MAX_TEXT_LENGTH = 2000


def validate_text(text: str) -> str:
    """Перевірити текст нотатки й повернути його без зайвих пробілів."""
    text = text.strip()
    if not text:
        raise ValueError("Note text cannot be empty.")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Note is too long (max {MAX_TEXT_LENGTH} characters).")
    return text


class Note:
    """Одна нотатка з текстом і тегами."""

    def __init__(self, note_id: int, text: str):
        self.id = note_id
        self.text = validate_text(text)
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.tags = []

    def add_tags(self, incoming_tags: list[str]) -> None:
        """Додати теги до цієї нотатки."""
        add_tags_to_list(self.tags, incoming_tags)

    def __setstate__(self, state:dict) -> None:
        """Відновити нотатку зі збережених даних"""
        self.__dict__.update(state)

        if "tags" not in state:
            self.tags = []    
        

    def edit(self, text: str) -> None:
        """Замінити текст нотатки."""
        self.text = validate_text(text)
        self.updated_at = datetime.now()

    def __str__(self) -> str:
        created = self.created_at.strftime("%d.%m.%Y %H:%M")
        return f"[{self.id}] {self.text}\n     created: {created}"


class NoteBook(UserDict):
    """Колекція нотаток; ключ - ID нотатки."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._next_id = max(self.data, default=0) + 1

    def add_note(self, text: str) -> Note:
        """Створити нотатку з новим унікальним ID (ID не використовуються повторно)."""
        note = Note(self._next_id, text)
        self.data[note.id] = note
        self._next_id += 1
        return note

    def get_note(self, note_id: int) -> Note:
        """Знайти нотатку за ID або ``KeyError`` з зрозумілим повідомленням."""
        try:
            return self.data[note_id]
        except KeyError:
            raise KeyError(f"Note with ID {note_id} not found.") from None

    def edit_note(self, note_id: int, text: str) -> Note:
        """Змінити текст нотатки за ID й повернути оновлену нотатку."""
        note = self.get_note(note_id)
        note.edit(text)
        return note

    def delete_note(self, note_id: int) -> None:
        """Видалити нотатку за ID. ``KeyError``, якщо такої немає."""
        self.get_note(note_id)
        del self.data[note_id]

    def find(self, query: str) -> list[Note]:
        """Пошук за підрядком у тексті (без урахування регістру)."""
        query = query.strip().lower()
        if not query:
            raise ValueError("Search query cannot be empty.")
        return [n for n in self.data.values() if query in n.text.lower()]

    def find_by_tag(self, incoming_tag: str) -> list[Note]:
        """Знайти нотатки за точним тегом."""
        matching_notes = []

        for note in self.data.values():
            if has_tag(note.tags, incoming_tag):
                matching_notes.append(note)

        return matching_notes

    def sort_by_tags(self) -> list[Note]:
        """Повернути нотатки, відсортовані за тегами."""

        def get_sort_key(note: Note) -> tuple[bool, list[str]]:
            return tag_sort_key(note.tags)

        return sorted(self.data.values(), key=get_sort_key)
