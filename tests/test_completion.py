"""Тести підказок під час набору: меню команд і нижня панель."""

from prompt_toolkit.completion import CompleteEvent
from prompt_toolkit.document import Document

from personal_assistant.cli import handlers  # noqa: F401  (реєструє команди)
from personal_assistant.cli.completion import (
    TOOLBAR_HINT,
    CommandCompleter,
    toolbar_text,
)


def _complete(text: str) -> dict[str, str]:
    """Підказки для набраного тексту: назва -> опис."""
    completer = CommandCompleter(["exit", "close"])
    found = completer.get_completions(Document(text), CompleteEvent())
    return {c.text: c.display_meta_text for c in found}


def test_completes_by_prefix_with_description():
    """На ``add`` пропонуються всі команди, що з нього починаються, з описом."""
    found = _complete("add")
    assert set(found) == {"add", "add-note", "add-phone"}
    assert found["add-note"] == "add-note <text> — add a text note"


def test_prefix_ignores_case():
    """Регістр набраного не важливий."""
    assert "show-notes" in _complete("SHOW-")


def test_exit_commands_are_suggested():
    """Команди виходу теж є в меню."""
    assert _complete("ex") == {"exit": "save and exit"}


def test_empty_input_lists_everything():
    """Порожній рядок — меню з усіма командами."""
    assert {"help", "add-note", "exit", "close"} <= set(_complete(""))


def test_no_completions_after_command_name():
    """Після пробілу йдуть аргументи — назви команд не підставляємо."""
    assert _complete("add John") == {}


def test_toolbar_shows_usage_of_typed_command():
    """Нижня панель показує формат команди, навіть коли вже пишуть аргументи."""
    expected = "edit <name> [field] [value] — "
    assert toolbar_text("edit John em").startswith(expected)
    assert toolbar_text("Edit").startswith(expected)


def test_toolbar_hint_for_unknown_or_empty():
    """Для порожнього або невідомого вводу — загальна підказка."""
    assert toolbar_text("") == TOOLBAR_HINT
    assert toolbar_text("ad") == TOOLBAR_HINT


def test_toolbar_exit():
    """Для команди виходу — її опис."""
    assert toolbar_text("exit", ["exit", "close"]) == "exit — save and exit"
