"""Головний цикл застосунку: читає команди і передає їх обробникам."""

import sys
from typing import Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import ANSI

from .cli import handlers  # noqa: F401  (реєструє всі команди)
from .cli import ui
from .cli.completion import CommandCompleter, toolbar_text
from .cli.handlers.general import EXIT_COMMANDS
from .cli.parser import parse_input
from .cli.prompts import OperationCancelled, confirm
from .cli.registry import COMMANDS
from .cli.suggest import guess_command
from .context import AppContext

PROMPT = "Enter a command: "
HELP_HINT = "Type 'help' to see all commands."


def _make_reader() -> Callable[[str], str]:
    """Функція читання команди.

    У терміналі — prompt_toolkit: меню команд з описами з'являється вже під
    час набору, внизу екрана — формат набраної команди, стрілки вгору/вниз
    гортають історію. Якщо ввід не з терміналу (наприклад, команди подано
    через pipe), prompt_toolkit не працює, тож беремо звичайний input.
    """
    if not sys.stdin.isatty():
        return lambda text: input(ui.prompt(text))
    session: PromptSession[str] = PromptSession(
        completer=CommandCompleter(EXIT_COMMANDS),
        complete_while_typing=True,
        bottom_toolbar=lambda: toolbar_text(
            get_app().current_buffer.text, EXIT_COMMANDS
        ),
    )
    # ANSI(): prompt_toolkit сам не розуміє кольорові коди colorama
    return lambda text: session.prompt(ANSI(ui.prompt(text)))


def _suggest_command(user_input: str, command: str, ctx: AppContext) -> str:
    """Невідома команда: вгадати, що мав на увазі користувач, і запропонувати.

    Якщо відомі й аргументи (опечатка в назві) або команда без обов'язкових
    аргументів — питаємо, чи виконати. Інакше показуємо, як її ввести.
    """
    guess = guess_command(user_input, [*COMMANDS, *EXIT_COMMANDS])
    is_phrase = len(user_input.split()) > 1 and (guess is None or guess.args is None)
    # Для фрази "I want to ..." назва команди 'i' нічого не каже користувачу
    unknown = ui.error(
        "Not sure what you mean." if is_phrase else f"Unknown command '{command}'."
    )
    if guess is None:
        return f"{unknown} {ui.info(HELP_HINT)}"

    if guess.command in EXIT_COMMANDS:
        # Вихід обробляє головний цикл, тож тут лише підказуємо
        return f"{unknown} Did you mean {ui.command_name(guess.command)}?"

    entry = COMMANDS[guess.command]
    args = guess.args
    if args is None and "<" not in entry.usage:
        args = []  # команді не потрібні аргументи — можна виконати одразу
    if args is None:
        return (
            f"{unknown} Maybe you want: {ui.command_name(entry.usage)}"
            f" - {entry.description}. {ui.info(HELP_HINT)}"
        )

    print(unknown)
    try:
        if not confirm(f"Did you mean '{guess.as_text()}'?"):
            return ui.info(HELP_HINT)
    except OperationCancelled:
        return ui.warning("Operation cancelled.")
    return entry.handler(args, ctx)


def run_command(user_input: str, ctx: AppContext) -> str:
    """Виконати один рядок вводу і повернути відповідь для виводу."""
    command, args = parse_input(user_input)
    entry = COMMANDS.get(command)
    if entry is None:
        return _suggest_command(user_input, command, ctx)
    return entry.handler(args, ctx)


def main() -> None:
    """Запустити застосунок; дані зберігаються після кожної команди і на виході."""
    ctx = AppContext.load()
    read = _make_reader()
    print(
        ui.title("Welcome to the personal assistant!")
        + ui.info(" Type 'help' to see all commands.")
    )
    try:
        while True:
            try:
                user_input = read(PROMPT)
            except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C
                print("\n" + ui.title("Good bye!"))
                break

            command, _ = parse_input(user_input)
            if not command:
                continue
            if command in EXIT_COMMANDS:
                print(ui.title("Good bye!"))
                break

            print(run_command(user_input, ctx))
            ctx.save()
    finally:
        ctx.save()


if __name__ == "__main__":
    main()
