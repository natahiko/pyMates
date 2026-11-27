# Personal Assistant — PyMates

Консольний «персональний помічник»: адресна книга з днями народження та нотатки.

- зберігає контакти: ім'я, телефони, email, адреса, день народження;
- показує, у кого день народження в найближчі N днів;
- перевіряє телефон, email та інші поля під час введення і перепитує, якщо значення некоректне;
- шукає контакти за будь-яким полем;
- редагує та видаляє контакти;
- зберігає текстові нотатки: додавання, пошук за текстом, редагування й видалення за ID;
- додає до нотаток теги, шукає й сортує нотатки за тегами;
- вгадує, що хотів користувач, якщо команду введено з помилкою або описано
  словами, і пропонує найближчу команду.

## Вимоги

- Python **3.10** або новіший
- Git

Перевірити версію Python:

```bash
python3 --version     # macOS / Linux
```

```powershell
py --version          # Windows
```

## Встановлення

### macOS / Linux

```bash
git clone https://github.com/natahiko/pyMates.git
cd pyMates
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
git clone https://github.com/natahiko/pyMates.git
cd pyMates
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Якщо PowerShell не дає активувати середовище, виконайте один раз
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
> У звичайному `cmd` активація: `.venv\Scripts\activate.bat`.

### Встановлення як пакета (необов'язково)

Після цього застосунок запускається командою `assistant` з будь-якої теки
(поки активне віртуальне середовище):

```bash
pip install -e .
```

## Запуск

З кореня репозиторію, з активованим віртуальним середовищем:

```bash
python main.py
```

Або так:

```bash
python -m personal_assistant
```

Або, якщо встановили як пакет:

```bash
assistant
```

Вийти: `exit`, `close`, `Ctrl+C` або `Ctrl+D`. Дані зберігаються після кожної команди.

## Сторонні бібліотеки

| Бібліотека | Для чого |
|---|---|
| [prompt_toolkit](https://python-prompt-toolkit.readthedocs.io/) | меню команд з описами під час набору, формат команди внизу екрана, історія команд стрілками ↑/↓ |
| [colorama](https://pypi.org/project/colorama/) | кольоровий вивід: успіх зеленим, помилки червоним, підказки жовтим (працює і у Windows) |
| [prettytable](https://pypi.org/project/prettytable/) | вивід контактів і днів народження таблицями |

Для розробки додатково: `black` (форматування), `flake8` (перевірка PEP 8), `pydocstyle` (наявність docstring), `pytest` (тести).

## Команди

Введіть `help`, щоб побачити список у самому застосунку.

Під час набору команди в терміналі з'являються підказки:

- **меню команд** — щойно почали набирати (`ad`), під рядком випадає список
  відповідних команд (`add`, `add-note`, `add-phone`) з форматом і описом
  кожної; вибір — стрілками ↑/↓ або `Tab`, підтвердження — `Enter`;
- **нижня панель** — показує формат набраної команди, наприклад
  `add-note <text> — add a text note`, тож видно, які аргументи
  ще треба ввести; поки команду не набрано — загальна підказка.

Підказки беруться з реєстру команд, тож нова команда з'являється в них сама.
Якщо команди подано через pipe (`... | python main.py`), підказок немає.

Регістр імен не важливий: `john` і `John` — той самий контакт.
Ім'я може складатися з кількох слів: `edit John Smith email ...`.

### Загальні

| Команда | Опис |
|---|---|
| `hello` | привітання |
| `help` | список усіх команд |
| `exit` / `close` | зберегти й вийти |

### Контакти

| Команда | Опис |
|---|---|
| `add [name]` | додати контакт; застосунок по черзі питає телефони, email, адресу, день народження |
| `all` | усі контакти таблицею |
| `show <name>` | один контакт |
| `search <text>` | пошук за ім'ям, телефоном, email, адресою або датою народження |
| `edit <name> [field] [value]` | змінити поле: `name`, `phone`, `email`, `address`, `birthday` |
| `add-phone <name> [phone]` | додати ще один телефон |
| `remove-phone <name> [phone]` | видалити телефон (без номера — вибір зі списку) |
| `clear <name> <field>` | очистити `phones`, `email`, `address` або `birthday` |
| `delete <name>` | видалити контакт (з підтвердженням) |
| `birthdays [days]` | дні народження від сьогодні до N днів уперед, за замовчуванням 7 |

### Нотатки

Нотатки не прив'язані до контактів. Кожна отримує числовий ID, за яким її
редагують і видаляють. ID не використовуються повторно: якщо видалити
нотатку 2, наступна нова отримає 3, а не 2.

| Команда | Опис |
|---|---|
| `add-note <text>` | додати нотатку; весь текст після команди — це її текст |
| `show-notes` | усі нотатки таблицею: ID, текст, теги, дата створення |
| `find-note <text>` | пошук нотаток за частиною тексту, без урахування регістру |
| `edit-note <id> <new text>` | замінити текст нотатки (теги лишаються) |
| `delete-note <id>` | видалити нотатку (з підтвердженням) |
| `tag-note <id> <tag> [more tags]` | додати до нотатки один або кілька тегів |
| `find-tag <tag>` | нотатки з цим тегом (лише один тег за раз) |
| `sort-notes` | усі нотатки, впорядковані за тегами |

#### Теги

Тег — ключове слово, що описує тему нотатки: `work`, `home`, `python`.

- **Теги розділяються пробілами:** `tag-note 1 work urgent` додає два теги.
  Кома не розділяє теги: `tag-note 1 work,urgent` створить один тег
  `work,urgent`.
- Регістр не важливий: теги зберігаються малими літерами, тож `Work` і `work`
  — той самий тег, а `find-tag WORK` знайде нотатки з тегом `work`.
- Однаковий тег двічі не додається; повторний `tag-note` лише дописує нові теги.
- `find-tag` шукає точний збіг: `find-tag wor` не знайде тег `work`.
  Для пошуку за частиною слова є `find-note`, але він шукає лише в тексті.
- `sort-notes` впорядковує нотатки за їхніми тегами за алфавітом (теги нотатки
  спершу сортуються, потім порівнюються по черзі); нотатки без тегів — у кінці.
- Видалити тег поки не можна.

### Якщо команду введено неправильно

Помічник пробує вгадати, що мали на увазі:

- опечатка в назві: `delet John` -> `delete John`, `addnote ...` -> `add-note ...`;
- опис словами: `I want to remove a phone` -> `remove-phone`,
  `who has birthday soon` -> `birthdays`. Для цього в тексті шукаються дія
  (`new`, `remove`, `find`, ...) і об'єкт (`note`, `phone`, `birthday`, ...).

Якщо команду можна виконати одразу, помічник питає `Did you mean ...? (y/n)`.
Якщо їй потрібні аргументи, яких з тексту не видно, — показує, як її ввести.

```text
Enter a command: addnote Купити молоко
Unknown command 'addnote'.
Did you mean 'add-note Купити молоко'? (y/n): y
Note added with ID 1.

Enter a command: I want to remove a phone
Not sure what you mean. Maybe you want: remove-phone <name> [phone] - remove a phone. Type 'help' to see all commands.
```

### Формати значень

| Поле | Формат | Приклад |
|---|---|---|
| Ім'я | 2–50 символів: літери, пробіл, `-`, `'`, `.` | `John Smith`, `Anna-Maria` |
| Телефон | 10 цифр; `+38`, пробіли, дужки й дефіси прибираються | `0661234567`, `+38 (066) 123-45-67` |
| Email | `name@domain.tld` | `john@example.com` |
| Адреса | довільний текст, 3–200 символів | `Kyiv, Khreshchatyk St, 1, apt 5` |
| День народження | `DD.MM.YYYY`, не в майбутньому | `25.11.1990` |
| Текст нотатки | 1–2000 символів; кілька пробілів поспіль стають одним | `Купити молоко і хліб` |
| ID нотатки | ціле число з `show-notes` | `3` |
| Тег | одне слово без пробілів; зберігається малими літерами | `work`, `python` |

### Як працює перевірка введення

Якщо значення некоректне, застосунок пояснює, що не так, і питає ще раз.
У будь-якому діалозі можна ввести `cancel` (або натиснути `Ctrl+C`) — дія
скасовується, нічого не змінюється. У майстрі `add` необов'язкове поле
пропускається порожнім `Enter`.

### Приклади

Додати контакт:

```text
Enter a command: add John Smith
New contact. Type 'cancel' at any step to abort.
Phone (Enter to skip): 066 123 45 67
Another phone (Enter to skip):
Email (Enter to skip): john@
Invalid email. Use a format like name@example.com. Try again or type 'cancel' to abort.
Email (Enter to skip): john@example.com
Address (e.g. Kyiv, Khreshchatyk St, 1, apt 5) (Enter to skip): Kyiv, Khreshchatyk St, 1
Birthday (DD.MM.YYYY) (Enter to skip): 25.11.1990
Contact 'John Smith' added.
```

Змінити поле одним рядком або через меню:

```text
Enter a command: edit John Smith email j.smith@mail.com
Contact updated.

Enter a command: edit John Smith
What do you want to change for John Smith?
  1. name
  2. phone
  3. email
  4. address
  5. birthday
Field: 1
New name: Johnny Smith
Contact updated.
```

Пошук і дні народження:

```text
Enter a command: search kyiv
Found 1 contact(s):
┌──────────────┬────────────┬──────────────────┬──────────────────────────┬────────────┐
│ Name         │ Phones     │ Email            │ Address                  │ Birthday   │
├──────────────┼────────────┼──────────────────┼──────────────────────────┼────────────┤
│ Johnny Smith │ 0661234567 │ j.smith@mail.com │ Kyiv, Khreshchatyk St, 1 │ 25.11.1990 │
└──────────────┴────────────┴──────────────────┴──────────────────────────┴────────────┘

Enter a command: birthdays 10
Birthdays in the next 10 day(s):
┌──────────────┬────────────┬──────────┬───────┐
│ Name         │ Date       │ When     │ Turns │
├──────────────┼────────────┼──────────┼───────┤
│ Johnny Smith │ 25.11.2026 │ tomorrow │ 36    │
└──────────────┴────────────┴──────────┴───────┘
```

Інші приклади:

```text
add-phone John Smith +380501112233
remove-phone John Smith 0501112233
clear John Smith address
delete John Smith
```

Нотатки:

```text
Enter a command: add-note Купити молоко і хліб
Note added with ID 1.

Enter a command: add-note Подзвонити мамі в неділю
Note added with ID 2.

Enter a command: find-note молоко
Found 1 note(s) for 'молоко':
┌────┬──────────────────────┬──────┬──────────────────┐
│ ID │ Note                 │ Tags │ Created          │
├────┼──────────────────────┼──────┼──────────────────┤
│ 1  │ Купити молоко і хліб │      │ 27.11.2026 10:30 │
└────┴──────────────────────┴──────┴──────────────────┘

Enter a command: edit-note 1 Купити молоко, хліб і сир
Note 1 updated.
┌────┬───────────────────────────┬──────┬──────────────────┐
│ ID │ Note                      │ Tags │ Created          │
├────┼───────────────────────────┼──────┼──────────────────┤
│ 1  │ Купити молоко, хліб і сир │      │ 27.11.2026 10:30 │
└────┴───────────────────────────┴──────┴──────────────────┘

Enter a command: delete-note 2
┌────┬──────────────────────────┬──────┬──────────────────┐
│ ID │ Note                     │ Tags │ Created          │
├────┼──────────────────────────┼──────┼──────────────────┤
│ 2  │ Подзвонити мамі в неділю │      │ 27.11.2026 10:30 │
└────┴──────────────────────────┴──────┴──────────────────┘
Delete note 2? (y/n): y
Note 2 deleted.

Enter a command: edit-note 9 Новий текст
Note 9 not found. Use 'show-notes' or 'find-note' to find it.
```

Теги (у нотатнику три нотатки, третя без тегів):

```text
Enter a command: tag-note 1 Shop home
Tags for note 1: shop, home

Enter a command: tag-note 2 work urgent
Tags for note 2: work, urgent

Enter a command: find-tag HOME
┌────┬──────────────────────┬────────────┬──────────────────┐
│ ID │ Note                 │ Tags       │ Created          │
├────┼──────────────────────┼────────────┼──────────────────┤
│ 1  │ Купити молоко і хліб │ home, shop │ 27.11.2026 10:30 │
└────┴──────────────────────┴────────────┴──────────────────┘

Enter a command: sort-notes
┌────┬──────────────────────────────┬──────────────┬──────────────────┐
│ ID │ Note                         │ Tags         │ Created          │
├────┼──────────────────────────────┼──────────────┼──────────────────┤
│ 1  │ Купити молоко і хліб         │ home, shop   │ 27.11.2026 10:30 │
│ 2  │ Підготувати звіт для команди │ urgent, work │ 27.11.2026 10:30 │
│ 3  │ Подзвонити мамі в неділю     │              │ 27.11.2026 10:30 │
└────┴──────────────────────────────┴──────────────┴──────────────────┘
```

## Тестові дані

Щоб заповнити книгу 10 тестовими контактами (для перевірки чи демо):

```bash
python -m personal_assistant.demo_data
```

Дні народження рахуються від сьогоднішньої дати, тож `birthdays` завжди
покаже кількох людей: сьогодні, завтра, за 3, 6 і 7 днів, а `birthdays 14` —
ще одну людину. Якщо в книзі вже є контакти, скрипт спитає підтвердження
і збереже стару книгу як `addressbook.pkl.bak` (`--force` — без питання).

Тестові нотатки (7 штук) — окремою командою:

```bash
python -m personal_assistant.demo_notes
```

Працює так само: якщо нотатки вже є, спитає підтвердження й збереже старі як
`notes.pkl.bak` (`--force` — без питання). Резервна копія одна: повторний
запуск перезапише її, тож справжні нотатки краще перевіряти в окремій теці
(див. нижче).

Щоб тестові дані не змішувались із робочими, можна взяти окрему теку:

```bash
PERSONAL_ASSISTANT_DATA_DIR=./demo python -m personal_assistant.demo_data
```

```bash
PERSONAL_ASSISTANT_DATA_DIR=./demo python main.py
```

У Windows (PowerShell) спершу `$env:PERSONAL_ASSISTANT_DATA_DIR = "demo"`, далі ті самі команди без префікса.

## Збереження даних

Формат — **pickle** (стандартна бібліотека Python): об'єкти зберігаються
разом зі своїми класами, тож не треба писати перетворення в JSON і назад.

Файли лежать у домашній теці користувача:

- macOS / Linux: `~/.personal_assistant/`
- Windows: `C:\Users\<user>\.personal_assistant\`

Контакти — у `addressbook.pkl`, нотатки — у `notes.pkl`.

Теку можна змінити змінною середовища `PERSONAL_ASSISTANT_DATA_DIR`
(зручно для демо з окремим набором даних). Запис атомарний: спершу у
тимчасовий файл, потім підміна. Пошкоджений файл не перезаписується мовчки,
а відкладається поруч як `*.broken`.

## Структура проєкту

```text
main.py                       # запуск: python main.py
personal_assistant/
├── app.py                    # головний цикл, prompt_toolkit
├── context.py                # AppContext: усі дані + завантаження/збереження
├── storage.py                # save_data / load_data (pickle)
├── demo_data.py              # тестові контакти: python -m personal_assistant.demo_data
├── demo_notes.py             # тестові нотатки: python -m personal_assistant.demo_notes
├── models/                   # класи даних, без вводу-виводу
│   ├── fields.py             # Field, Name, Phone, Email, Address, Birthday
│   ├── record.py             # Record — один контакт
│   ├── address_book.py       # AddressBook — пошук, дні народження
│   ├── notes.py              # Note, NoteBook — нотатки за ID, пошук, сортування за тегами
│   └── tags.py               # допоміжні функції для тегів: додавання, пошук, ключ сортування
└── cli/                      # усе, що стосується консолі
    ├── registry.py           # @command — реєстрація команд
    ├── decorators.py         # input_error — помилки -> повідомлення
    ├── prompts.py            # ask_valid, confirm, choose, cancel
    ├── ui.py                 # кольори й таблиці
    ├── parser.py             # розбір введеного рядка
    ├── suggest.py            # вгадування команди за опечаткою чи змістом
    ├── completion.py         # меню команд і нижня панель під час набору
    └── handlers/
        ├── general.py        # hello, help
        ├── contacts.py       # команди контактів
        └── notes.py          # команди нотаток
tests/                        # автотести (pytest), див. розділ «Тести»
├── conftest.py               # спільні фікстури: ctx, answers; вимикає кольори
├── test_models.py            # валідація полів, Record, AddressBook
├── test_contacts_commands.py # команди контактів з імітацією вводу
├── test_storage.py           # збереження й пошкоджені файли
├── test_demo_data.py         # генератор тестових даних
├── test_suggest.py           # вгадування команди
├── test_completion.py        # меню команд і нижня панель
└── test_ui.py                # кольори й таблиці
```

## Для розробників

### Налаштування

```bash
pip install -r requirements-dev.txt
```

Перед кожним PR:

```bash
black .
```

```bash
flake8
```

```bash
pydocstyle personal_assistant tests
```

```bash
pytest
```

### Тести

Автотести перевіряють логіку без ручного вводу — за секунду, після кожної зміни.
Запуск із кореня проєкту (потрібен `requirements-dev.txt`):

```bash
pytest
```

Корисні варіанти:

```bash
pytest -v                          # кожен тест окремим рядком
```

```bash
pytest tests/test_models.py        # лише один файл
```

```bash
pytest -k email                    # лише тести, у назві яких є "email"
```

У PyCharm: правий клік на теці `tests` → **Run 'pytest in tests'**.
Якщо PyCharm запускає тести не через pytest, оберіть його в
Settings → Tools → Python Integrated Tools → Default test runner.

Що покривають тести:

| Файл | Що перевіряє |
|---|---|
| `test_models.py` | валідацію імені, телефону, email, адреси й дати; телефони контакту; пошук за будь-яким полем; перейменування, видалення, дублікати; дні народження в межах N днів, зокрема перехід через Новий рік |
| `test_contacts_commands.py` | команди `add`, `edit`, `search`, `delete` так, як їх вводить користувач: повторний запит після помилки, `cancel`, підтвердження y/n, зрозумілі повідомлення замість падінь |
| `test_storage.py` | збереження й завантаження; відсутній файл; пошкоджений файл відкладається як `.broken` |
| `test_demo_data.py` | тестові контакти проходять валідацію, а `birthdays` завжди має що показати (і 29 лютого теж) |
| `test_suggest.py` | вгадування команди: опечатки, злиті слова, опис словами; підтвердження y/n перед виконанням |
| `test_completion.py` | меню команд за початком назви (з описами, без урахування регістру), нижня панель з форматом команди |
| `test_ui.py` | коли вмикаються кольори, і що вони не ламають таблиці |

#### Як написати тест для своєї команди

Діалоги читають ввід через `prompts.input_func`, тож у тесті його можна
підмінити списком готових відповідей. Для цього в `tests/conftest.py` є
фікстури, доступні в будь-якому файлі тестів без імпорту:

- `ctx` — порожній `AppContext` (дані лише в пам'яті, файли не чіпаються);
- `answers` — список відповідей, які по черзі отримають діалоги.

Приклад:

```python
from personal_assistant.app import run_command


def test_delete_note_needs_confirmation(ctx, answers):
    """Нотатка видаляється лише після відповіді y."""
    ctx.notes.add_note("Buy milk")
    answers += ["maybe", "n"]  # спершу незрозуміла відповідь, потім "ні"
    result = run_command("delete-note 1", ctx)
    assert "Nothing deleted" in result
    assert len(ctx.notes) == 1
    assert answers == []  # усі відповіді використані
```

Кольори в тестах вимкнені (`conftest.py`), тож результат команди — звичайний текст.

### Як додати нову команду

Готовий приклад — `personal_assistant/cli/handlers/notes.py`.

1. Додайте функцію в модуль своєї групи в `personal_assistant/cli/handlers/`
   або створіть новий модуль.
2. Зареєструйте команду декоратором — вона одразу з'явиться в `help` і в автодоповненні:

   ```python
   from ...context import AppContext
   from .. import ui
   from ..registry import command, require_args

   GROUP = "Notes"


   @command("count-notes", "count-notes", "show how many notes are saved", GROUP)
   def count_notes(_args: list[str], ctx: AppContext) -> str:
       """Показати кількість нотаток."""
       return ui.success(f"You have {len(ctx.notes)} note(s).")
   ```

3. Якщо створили новий модуль, додайте його імпорт у
   `personal_assistant/cli/handlers/__init__.py`.

Помилки валідації кидайте як `ValueError("текст для користувача")`, «не знайдено» —
як `NotFoundError("Note 3 not found.")`; декоратор сам покаже їх червоним.

### Як додати нову колекцію даних

Так додано нотатки, тож їх зручно взяти за зразок:

1. Клас моделі — у `personal_assistant/models/` (як `models/notes.py`) і його
   експорт у `models/__init__.py`.
2. У `personal_assistant/context.py` — назва файлу, поле в `AppContext` і рядки
   в `load` / `save`:

   ```python
   NOTES_FILE = "notes.pkl"

   @dataclass
   class AppContext:
       book: AddressBook
       notes: NoteBook

       @classmethod
       def load(cls) -> "AppContext":
           return cls(
               book=load_data(data_file(ADDRESS_BOOK_FILE), AddressBook),
               notes=load_data(data_file(NOTES_FILE), NoteBook),
           )

       def save(self) -> None:
           save_data(self.book, data_file(ADDRESS_BOOK_FILE))
           save_data(self.notes, data_file(NOTES_FILE))
   ```

3. Додайте нове поле у фікстуру `ctx` у `tests/conftest.py`, інакше тести
   впадуть з `TypeError: ... missing 1 required positional argument`.

### Стиль коду

- PEP 8, довжина рядка 88 (як у black);
- docstring у кожної функції, класу й модуля;
- коментарі — лише до неочевидної логіки;
- кожна задача — окрема гілка й pull request у `main`.

## Команда

| Роль | Учасник |
|---|---|
| Team Lead | _TBD_ |
| Scrum Master | _TBD_ |
| Developer | _TBD_ |
