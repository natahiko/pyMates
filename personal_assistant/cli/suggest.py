"""Вгадування команди за введеним текстом, якщо такої команди немає.

Дві стратегії, по черзі:

1. Опечатка. Назву порівнюємо з усіма командами (``delet`` -> ``delete``).
   Пробуємо й злити перші два слова: ``add note ...`` -> ``add-note ...``.
   Тут аргументи зрозумілі, тож команду можна одразу виконати.
2. Намір. Шукаємо в тексті дію (``new``, ``remove``, ``find`` ...) і
   об'єкт (``note``, ``phone``, ``birthday`` ...) і за парою підбираємо
   команду: ``I want to remove a phone`` -> ``remove-phone``. Аргументи тут
   вгадати не можна, тож пропонуємо лише саму команду.
"""

import re
from dataclasses import dataclass
from difflib import SequenceMatcher, get_close_matches
from typing import Iterable, Optional

# Наскільки назва має бути схожа на команду, щоб вважати її опечаткою (0..1)
TYPO_CUTOFF = 0.75
# Те саме для окремих слів у тексті (``birthdys`` -> ``birthdays``)
WORD_CUTOFF = 0.8
# Коротші слова не виправляємо: ``on`` легко «схоже» на будь-що
MIN_FUZZY_WORD = 4

# Дія -> слова, якими її описують
VERBS: dict[str, set[str]] = {
    "add": {"add", "new", "create", "save", "write", "make", "remember", "insert"},
    "remove": {"remove", "delete", "del", "erase", "drop", "rm", "forget"},
    "find": {"find", "search", "lookup", "look", "where", "who", "which"},
    "show": {"show", "list", "view", "display", "print", "see", "get", "all"},
    "edit": {"edit", "change", "update", "modify", "rename", "fix", "correct"},
    "clear": {"clear", "reset", "empty", "wipe"},
    "sort": {"sort", "order", "arrange", "group"},
    "tag": {"tag", "label", "mark"},
    "greet": {"hi", "hello", "hey"},
    "help": {"help", "commands", "how", "what"},
}

# Об'єкт -> слова, якими його називають
OBJECTS: dict[str, set[str]] = {
    "note": {"note", "notes", "memo", "memos", "todo", "reminder"},
    "tag": {"tag", "tags", "label", "labels"},
    "phone": {"phone", "phones", "number", "numbers", "mobile", "tel", "call"},
    "birthday": {"birthday", "birthdays", "bday", "born", "birth", "anniversary"},
    "contact": {
        "contact",
        "contacts",
        "person",
        "people",
        "friend",
        "friends",
        "address",
        "email",
        "book",
    },
}

# (дія, об'єкт) -> команда; ``None`` — об'єкт або дію не названо
INTENTS: dict[tuple[Optional[str], Optional[str]], str] = {
    ("add", "note"): "add-note",
    ("remove", "note"): "delete-note",
    ("find", "note"): "find-note",
    ("show", "note"): "show-notes",
    ("edit", "note"): "edit-note",
    ("sort", "note"): "sort-notes",
    ("tag", "note"): "tag-note",
    ("add", "tag"): "tag-note",
    ("tag", "tag"): "tag-note",
    ("find", "tag"): "find-tag",
    ("show", "tag"): "find-tag",
    ("sort", "tag"): "sort-notes",
    ("add", "phone"): "add-phone",
    ("remove", "phone"): "remove-phone",
    ("edit", "phone"): "edit",
    ("clear", "phone"): "clear",
    ("find", "phone"): "search",
    ("show", "phone"): "show",
    ("add", "birthday"): "edit",
    ("edit", "birthday"): "edit",
    ("clear", "birthday"): "clear",
    ("find", "birthday"): "birthdays",
    ("show", "birthday"): "birthdays",
    ("add", "contact"): "add",
    ("remove", "contact"): "delete",
    ("find", "contact"): "search",
    ("show", "contact"): "all",
    ("edit", "contact"): "edit",
    ("clear", "contact"): "clear",
    ("add", None): "add",
    ("remove", None): "delete",
    ("find", None): "search",
    ("show", None): "all",
    ("edit", None): "edit",
    ("clear", None): "clear",
    ("sort", None): "sort-notes",
    ("tag", None): "tag-note",
    ("greet", None): "hello",
    ("help", None): "help",
    (None, "note"): "show-notes",
    (None, "tag"): "find-tag",
    (None, "phone"): "add-phone",
    (None, "birthday"): "birthdays",
    (None, "contact"): "all",
}


@dataclass(frozen=True)
class Guess:
    """Найімовірніша команда.

    ``args`` — аргументи для неї, якщо їх вдалося зберегти (опечатка в
    назві), або ``None``, якщо команду вгадано лише за змістом.
    """

    command: str
    args: Optional[list[str]]

    def as_text(self) -> str:
        """Рядок, який виконається: ``add-note buy milk``."""
        return " ".join([self.command, *(self.args or [])])


def _squash(name: str) -> str:
    """Прибрати дефіси й підкреслення: ``add-note`` / ``add_note`` -> ``addnote``."""
    return name.replace("-", "").replace("_", "")


def _similarity(a: str, b: str) -> float:
    """Схожість двох назв від 0 до 1, без урахування дефісів."""
    return SequenceMatcher(None, _squash(a), _squash(b)).ratio()


def guess_typo(command: str, args: list[str], names: Iterable[str]) -> Optional[Guess]:
    """Команда, схожа на введену назву, або ``None``.

    Розглядаємо два варіанти: сама назва (``delet John``) і назва, злита з
    першим аргументом (``add note buy milk`` -> ``add-note``). Беремо
    найсхожіший; за однакової схожості перемагає перший варіант.
    """
    variants = [(command, args)]
    if args:
        variants.append((command + "-" + args[0].lower(), args[1:]))

    best: Optional[Guess] = None
    best_score = TYPO_CUTOFF
    for typed, rest in variants:
        for name in names:
            score = _similarity(typed, name)
            if score > best_score or (score == best_score and best is None):
                best, best_score = Guess(name, list(rest)), score
    return best


def _words(text: str) -> list[str]:
    """Слова тексту малими літерами, без розділових знаків і дефісів."""
    return re.findall(r"[a-z]+", text.lower())


def _match_word(word: str, vocabulary: dict[str, set[str]]) -> Optional[str]:
    """Ключ словника, до якого належить слово (з поправкою на опечатки)."""
    for key, synonyms in vocabulary.items():
        if word in synonyms:
            return key
    if len(word) < MIN_FUZZY_WORD:
        return None
    all_words = {w: key for key, synonyms in vocabulary.items() for w in synonyms}
    close = get_close_matches(word, all_words, n=1, cutoff=WORD_CUTOFF)
    return all_words[close[0]] if close else None


def guess_intent(text: str) -> Optional[str]:
    """Команда, яку описує текст словами, або ``None``.

    Беремо першу знайдену дію і перший знайдений об'єкт. Слово може бути
    і тим, і тим (``tag``) — тоді воно рахується як дія, якщо дії ще нема.
    """
    verb: Optional[str] = None
    obj: Optional[str] = None
    for word in _words(text):
        word_verb = _match_word(word, VERBS)
        word_obj = _match_word(word, OBJECTS)
        if verb is None and word_verb is not None:
            verb = word_verb
        elif obj is None and word_obj is not None:
            obj = word_obj
    if verb is None and obj is None:
        return None
    return INTENTS.get((verb, obj)) or INTENTS.get((verb, None))


def guess_command(user_input: str, names: Iterable[str]) -> Optional[Guess]:
    """Найближча команда до введеного рядка, або ``None``, якщо нічого схожого."""
    names = list(names)
    parts = user_input.split()
    if not parts:
        return None
    typo = guess_typo(parts[0].lower(), parts[1:], names)
    if typo is not None:
        return typo
    intent = guess_intent(user_input)
    if intent is not None and intent in names:
        return Guess(intent, None)
    return None
