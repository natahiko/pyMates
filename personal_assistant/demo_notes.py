"""Заповнити нотатник тестовими нотатками для перевірки й демо.

Запуск: ``python -m personal_assistant.demo_notes``

Наявний нотатник перед перезаписом відкладаємо в ``.bak``.
"""

import sys

from .context import NOTES_FILE
from .models import NoteBook
from .storage import data_file, load_data, save_data

DEMO_NOTES: list[str] = [
    "Блекаут: поки є світло, поставити на зарядку EcoFlow, павербанк для "
    "роутера та ліхтарик у коридорі. Заодно закинути прання на швидкий "
    "режим, бо за графіком відключення о 16:00",
    "Донат: закинути 500 грн на монобанку або актуальний збір, поки все "
    "не пішло на каву і доставку",
    "Сусіди та генератор: написати в чат будинку, чи скидаємося на пальне "
    "для генератора на ліфт, бо підніматися на 14-й поверх із пакетами "
    "з АТБ — так собі кардіо",
    "GitHub: перестати заливати файли через веб-інтерфейс. Подивитися "
    "туторіал з git commit і git push у терміналі та зрозуміти, що таке "
    "pull request, щоб не зламати main",
    "Промпт-інжиніринг: протестувати новий системний промпт для бота, щоб "
    "він не вигадував факти, відповідав по базі знань і сам ставив теги "
    "нотаткам",
    "Курс з Python: доробити всю домашку до понеділка 30.11.2026, дедлайн горить",
    "Ідея для пет-проєкту: телеграм-бот, який парсить графіки ДТЕК і за "
    "15 хвилин до відключення присилає мем та нагадування зберегти всі "
    "відкриті документи",
]


def build_demo_notebook() -> NoteBook:
    """Створити нотатник з тестовими нотатками."""
    notebook = NoteBook()
    for text in DEMO_NOTES:
        notebook.add_note(text)
    return notebook


def main() -> None:
    """Записати тестові нотатки у файл даних, зберігши копію старого."""
    path = data_file(NOTES_FILE)
    if path.exists():
        existing = load_data(path, NoteBook)
        if existing and "--force" not in sys.argv:
            try:
                answer = input(
                    f"{path} already has {len(existing)} note(s). "
                    "Replace them with demo data? A backup will be kept (y/n): "
                )
            except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C = "ні"
                answer = ""
                print()
            if answer.strip().lower() not in ("y", "yes"):
                print("Nothing changed.")
                return
        if path.exists():
            backup = path.with_suffix(path.suffix + ".bak")
            path.replace(backup)
            print(f"Old data saved to {backup}")

    notebook = build_demo_notebook()
    save_data(notebook, path)
    print(f"Saved {len(notebook)} demo notes to {path}")


if __name__ == "__main__":
    main()
