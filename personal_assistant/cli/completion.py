"""Підказки в терміналі під час набору команди (prompt_toolkit).

- ``CommandCompleter`` — меню команд, що з'являється вже під час набору,
  з описом біля кожної;
- ``toolbar_text`` — рядок унизу екрана з форматом команди, яку набирають.

Усе береться з реєстру ``COMMANDS``, тож нова команда з'являється тут сама.
"""

from typing import Iterable

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document

from .registry import COMMANDS

EXIT_DESCRIPTION = "save and exit"
TOOLBAR_HINT = "Start typing a command, ↑/↓ or Tab to choose. 'help' — all commands."


class CommandCompleter(Completer):
    """Доповнює назву команди (перше слово) і показує її опис."""

    def __init__(self, exit_commands: Iterable[str] = ()):
        """``exit_commands`` — команди виходу, яких немає в реєстрі."""
        self.exit_commands = tuple(exit_commands)

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        """Команди, що починаються з набраного; після пробілу — нічого."""
        text = document.text_before_cursor.lstrip()
        if " " in text:
            return  # назву вже введено, далі йдуть аргументи
        typed = text.lower()
        for name, entry in COMMANDS.items():
            if name.startswith(typed):
                yield Completion(
                    name,
                    start_position=-len(text),
                    display_meta=f"{entry.usage} — {entry.description}",
                )
        for name in self.exit_commands:
            if name.startswith(typed):
                yield Completion(
                    name, start_position=-len(text), display_meta=EXIT_DESCRIPTION
                )


def toolbar_text(text: str, exit_commands: Iterable[str] = ()) -> str:
    """Текст нижньої панелі для вже набраного рядка.

    Якщо перше слово — відома команда, показуємо її формат і опис,
    інакше — загальну підказку.
    """
    parts = text.split()
    name = parts[0].lower() if parts else ""
    entry = COMMANDS.get(name)
    if entry is not None:
        return f"{entry.usage} — {entry.description}"
    if name in exit_commands:
        return f"{name} — {EXIT_DESCRIPTION}"
    return TOOLBAR_HINT
