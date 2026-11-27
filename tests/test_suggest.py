"""Тести вгадування команди за введеним текстом."""

import pytest

from personal_assistant.app import run_command
from personal_assistant.cli.handlers.general import EXIT_COMMANDS
from personal_assistant.cli.registry import COMMANDS
from personal_assistant.cli.suggest import Guess, guess_command

NAMES = [*COMMANDS, *EXIT_COMMANDS]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("delet John", Guess("delete", ["John"])),
        ("serch kyiv", Guess("search", ["kyiv"])),
        ("addnote buy milk", Guess("add-note", ["buy", "milk"])),
        ("add_note buy milk", Guess("add-note", ["buy", "milk"])),
        ("shownotes", Guess("show-notes", [])),
        ("tag note 1 work", Guess("tag-note", ["1", "work"])),
        ("Birthday", Guess("birthdays", [])),
        ("exti", Guess("exit", [])),
    ],
)
def test_typo_keeps_arguments(text, expected):
    """Опечатку в назві виправляємо, аргументи зберігаємо."""
    assert guess_command(text, NAMES) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("I want to remove a phone", "remove-phone"),
        ("new note", "add-note"),
        ("who has birthday soon", "birthdays"),
        ("sort by tags", "sort-notes"),
        ("change email of John", "edit"),
        ("list all contacts", "all"),
        ("please erase this contact", "delete"),
        ("look for a memo", "find-note"),
        ("upcoming birthdys", "birthdays"),  # опечатка в слові
    ],
)
def test_intent_from_words(text, expected):
    """Команду вгадуємо за змістом фрази; аргументи невідомі."""
    assert guess_command(text, NAMES) == Guess(expected, None)


@pytest.mark.parametrize("text", ["fly", "xyz abc", ""])
def test_nothing_similar(text):
    """Якщо нічого схожого нема — нічого не вигадуємо."""
    assert guess_command(text, NAMES) is None


def test_confirmed_typo_runs_command(ctx, answers):
    """Після «y» виправлена команда виконується з тими самими аргументами."""
    answers += ["y"]
    result = run_command("addnote Buy milk", ctx)
    assert "added" in result
    assert ctx.notes.find("milk")
    assert answers == []


def test_declined_typo_does_nothing(ctx, answers):
    """Після «n» нічого не виконується."""
    answers += ["n"]
    result = run_command("addnote Buy milk", ctx)
    assert "help" in result
    assert len(ctx.notes) == 0


def test_cancel_typo_question(ctx, answers):
    """На питання «Did you mean» можна відповісти cancel."""
    answers += ["cancel"]
    assert "cancelled" in run_command("addnote Buy milk", ctx)
    assert len(ctx.notes) == 0


def test_intent_without_args_is_offered_to_run(ctx, answers):
    """Команду без обов'язкових аргументів пропонуємо одразу виконати."""
    ctx.notes.add_note("Buy milk")
    answers += ["y"]
    assert "Buy milk" in run_command("my notes please", ctx)
    assert answers == []


def test_intent_with_required_args_shows_usage(ctx):
    """Якщо команді потрібні аргументи — показуємо, як її ввести."""
    result = run_command("I want to remove a phone", ctx)
    assert "remove-phone <name> [phone]" in result


def test_exit_typo_only_hints(ctx):
    """Вихід не виконується з run_command — лише підказка."""
    assert "exit" in run_command("exti", ctx)


def test_phrase_does_not_show_first_word_as_command(ctx):
    """Для фрази не пишемо «Unknown command 'i'»."""
    result = run_command("I want to remove a phone", ctx)
    assert "Not sure what you mean" in result
    assert "'i'" not in result
    assert "Unknown command 'fly'" in run_command("fly", ctx)
