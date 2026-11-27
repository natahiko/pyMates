"""Команди для роботи з нотатками."""

from ...context import AppContext
from ...models.notes import Note
from .. import prompts, ui
from .. decorators import NotFoundError
from .. registry import command, require_args

GROUP = "Notes"
NOTE_HEADERS = ("ID", "Note", "Tags", "Created")

def _parse_id(value: str) -> int:
    """Перетворити рядок на числовий ID нотатки."""
    if not value.isdigit():
        raise ValueError(f"'{value}' is not a valid note ID (use a number).")
    return int(value)


def _get_note_or_raise(ctx: AppContext, note_id: int) -> Note:
    """Повернути нотатку за ID або кинути NotFoundError."""
    try:
        return ctx.notes.get_note(note_id)
    except KeyError as error:
        raise NotFoundError(
            f"Note {note_id} not found. Use 'show-notes' or 'find-note' to find it."
        ) from error


def _notes_table(notes: list[Note]) -> str:
    """Сформувати таблицю нотаток."""
    rows = (
        (
            ui.highlight(str(n.id)),
            n.text,
            ", ".join(sorted(n.tags)),
            n.created_at.strftime("%d.%m.%Y %H:%M"),
        )
        for n in notes
    )
    return ui.table(NOTE_HEADERS, rows)


@command("add-note", "add-note <text>", "add a text note", GROUP)
def add_note(args: list[str], ctx: AppContext) -> str:
    """Додати нову текстову нотатку."""
    require_args(args, 1, "add-note")
    note = ctx.notes.add_note(" ".join(args))
    return ui.success(f"Note added with ID {note.id}.")

@command(
    "tag-note",
    "tag-note <id> <tag> [more tags]",
    "add tags to a note by ID",
    GROUP,
)
def tag_note(args: list[str], ctx: AppContext) -> str:
    """Додати теги до нотатки за її ID."""
    require_args(args, 2, "tag-note")
    note_id = _parse_id(args[0])
    note = _get_note_or_raise(ctx, note_id)

    note.add_tags(args[1:])

    tags_text = ", ".join(note.tags)
    return ui.success(f"Tags for note {note.id}: {tags_text}")


@command("show-notes", "show-notes", "show all saved notes", GROUP)
def show_notes(_args: list[str], ctx: AppContext) -> str:
    """Показати всі збережені нотатки."""
    notes = list(ctx.notes.values())
    if not notes:
        return ui.warning("No notes saved. Use 'add-note' to create one.")
    return _notes_table(notes)


@command("find-note", "find-note <query>", "search notes by text", GROUP)
def find_note(args: list[str], ctx: AppContext) -> str:
    """Пошук нотаток за підрядком у тексті (без урахування регістру)."""
    require_args(args, 1, "find-note")
    query = " ".join(args)
    found = ctx.notes.find(query)
    if not found:
        return ui.warning(f"No notes match '{query}'.")
    header = ui.title(f"Found {len(found)} note(s) for '{query}':")
    return header + "\n" + _notes_table(found)

@command("find-tag", "find-tag <tag>", "find notes by tag", GROUP)
def find_tag(args: list[str], ctx: AppContext) -> str:
    """Знайти нотатки за тегом."""
    if len(args) != 1:
        raise ValueError("Usage: find-tag <tag>.")

    incoming_tag = args[0]
    matching_notes = ctx.notes.find_by_tag(incoming_tag)

    if not matching_notes:
        return ui.warning(f"No notes found with tag '{incoming_tag}'.")

    return _notes_table(matching_notes)

@command("sort-notes", "sort-notes", "sort notes by tags", GROUP)
def sort_notes(args: list[str], ctx: AppContext) -> str:
    """Показати нотатки, відсортовані за тегами."""
    if args:
        raise ValueError("Usage: sort-notes.")

    notes = ctx.notes.sort_by_tags()

    if not notes:
        return ui.warning("No notes saved. Use 'add-note' to create one.")

    return _notes_table(notes)

@command("edit-note", "edit-note <id> <new text>", "edit a note by ID", GROUP)
def edit_note(args: list[str], ctx: AppContext) -> str:
    """Змінити текст нотатки за ID."""
    require_args(args, 2, "edit-note")
    note_id = _parse_id(args[0])
    _get_note_or_raise(ctx, note_id)
    new_text = " ".join(args[1:])
    note = ctx.notes.edit_note(note_id, new_text)
    return ui.success(f"Note {note.id} updated.") + "\n" + _notes_table([note])


@command("delete-note", "delete-note <id>", "delete a note by ID", GROUP)
def delete_note(args: list[str], ctx: AppContext) -> str:
    """Видалити нотатку за ID після підтвердження."""
    require_args(args, 1, "delete-note")
    note_id = _parse_id(args[0])
    note = _get_note_or_raise(ctx, note_id)
    print(_notes_table([note]))
    if not prompts.confirm(f"Delete note {note_id}?"):
        return ui.warning("Nothing deleted.")
    ctx.notes.delete_note(note_id)
    return ui.success(f"Note {note_id} deleted.")
