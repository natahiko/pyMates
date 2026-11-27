"""Допоміжні функції для роботи з тегами нотаток."""


def add_tags(current_tags, incoming_tags):
    """Додати нові теги до списку без повторів."""
    for incoming_tag in incoming_tags:
        tag = incoming_tag.strip().lower()

        if tag and tag not in current_tags:
            current_tags.append(tag)

def has_tag(current_tags, incoming_tag):
    """Перевірити, чи є тег у списку."""
    tag = incoming_tag.strip().lower()
    return tag in current_tags

def tag_sort_key(current_tags):
    """Підготувати ключ для сортування нотатки за тегами."""
    has_no_tags = not current_tags
    sorted_tags = sorted(current_tags)

    return has_no_tags, sorted_tags