<div align="center">
<p align="center">
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/logo.png" alt="pykeyboard">
</p>

![PyPI](https://img.shields.io/pypi/v/pykeyboard-kurigram)
[![Downloads](https://pepy.tech/badge/pykeyboard-kurigram)](https://pepy.tech/project/pykeyboard-kurigram)
![Python Version](https://img.shields.io/pypi/pyversions/pykeyboard-kurigram)

![License](https://img.shields.io/github/license/johnnie-610/pykeyboard)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/johnnie-610/pykeyboard/actions)
[![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-brightgreen)](https://github.com/johnnie-610/pykeyboard)

 <p><h2>🚀 Modern, Type-Safe Keyboard Library for <a href="https://pypi.org">Kurigram</a> 🚀</h2></p>
 <br>
 <p><strong><em>Built with Pydantic • 50+ Languages • Full Type Safety • Comprehensive Testing</em></strong></p>
 <br>
 <p><strong><em>README last updated:  </em></strong></p>

</div>

# PyKeyboard

**PyKeyboard** is a modern, fully type-safe Python library for creating beautiful and functional inline and reply keyboards for Telegram bots using [Kurigram](https://github.com/KurimuzonAkuma/pyrogram).

## ✨ Key Features

- 🎯 **Full Type Safety** - Built with Pydantic v2 for runtime validation and IDE support
- 🌍 **50+ Languages** - Comprehensive locale support with native language names and flags
- 🧪 **100% Test Coverage** - Extensive test suite with pytest and coverage reporting
- 🔍 **Static Analysis** - MyPy, Ruff, and Pyright integration for code quality
- 📦 **JSON Serialization** - Built-in keyboard serialization/deserialization
- 🚀 **Modern Python** - Uses latest Python features and best practices
- 🎨 **Beautiful API** - Intuitive, chainable methods for keyboard construction
- 🛡️ **Error Handling** - Comprehensive validation with descriptive error messages

## Table of Contents

- [PyKeyboard](#pykeyboard)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Features](#features)
  - [Inline Keyboard](#inline-keyboard)
  - [Reply Keyboard](#reply-keyboard)
  - [Pagination](#pagination)
  - [Language Selection](#language-selection)
  - [Type Safety](#type-safety)
  - [Serialization](#serialization)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## 📦 Installation

```bash
# Using pip
pip install pykeyboard-kurigram

# Using poetry
poetry add pykeyboard-kurigram

# For development
git clone https://github.com/johnnie-610/pykeyboard.git
cd pykeyboard
poetry install
```

## 🚀 Quick Start

```python
from pykeyboard import InlineKeyboard, InlineButton

# Create a simple inline keyboard
keyboard = InlineKeyboard()
keyboard.add(
    InlineButton("👍 Like", "action:like"),
    InlineButton("👎 Dislike", "action:dislike"),
    InlineButton("📊 Stats", "action:stats")
)

# Use with Kurigram
await message.reply_text("What do you think?", reply_markup=keyboard.pyrogram_markup)
```

## 🎯 Features

### Inline Keyboard

Create sophisticated inline keyboards with ease:

```python
from pykeyboard import InlineKeyboard, InlineButton

keyboard = InlineKeyboard(row_width=2)
keyboard.add(
    InlineButton("Option 1", "choice:1"),
    InlineButton("Option 2", "choice:2"),
    InlineButton("Option 3", "choice:3"),
    InlineButton("Cancel", "action:cancel")
)
```

### Reply Keyboard

Build reply keyboards with full customization:

```python
from pykeyboard import ReplyKeyboard, ReplyButton

keyboard = ReplyKeyboard(resize_keyboard=True, one_time_keyboard=True)
keyboard.row(
    ReplyButton("📱 Contact", request_contact=True),
    ReplyButton("📍 Location", request_location=True)
)
keyboard.row(ReplyButton("❌ Cancel"))
```

### Pagination

Advanced pagination with customizable navigation:

```python
keyboard = InlineKeyboard()
keyboard.paginate(
    count_pages=25,
    current_page=12,
    callback_pattern="page:{number}"
)
# Creates: « 1 ‹ 11 · 12 · 13 › 25 »
```

### Language Selection

Choose from 50+ supported languages:

```python
keyboard = InlineKeyboard()
keyboard.languages(
    callback_pattern="lang:{locale}",
    locales=["en_US", "es_ES", "fr_FR", "de_DE", "ru_RU"],
    row_width=2
)
```

### Type Safety

Full type safety with Pydantic validation:

```python
from pykeyboard import InlineButton

# This will raise a validation error at runtime
try:
    button = InlineButton("", "callback")  # Empty text not allowed
except ValueError as e:
    print(f"Validation error: {e}")

# Full IDE support and autocompletion
button: InlineButton = InlineButton(
    text="Click me",
    callback_data="action:click",
    url="https://example.com"  # Optional URL
)
```

### Serialization

Built-in JSON serialization for persistence:

```python
# Serialize keyboard to JSON
keyboard_data = keyboard.to_dict()
json_str = keyboard.model_dump_json()

# Deserialize from JSON
restored_keyboard = InlineKeyboard.from_dict(keyboard_data)
```

## 📖 Detailed Documentation

### Inline Keyboard

```python
from pykeyboard import InlineKeyboard
```

#### Parameters

- `row_width` (int, default 3): Number of buttons per row

#### Basic Usage

##### Adding Buttons

```python
from pykeyboard import InlineKeyboard, InlineButton

keyboard = InlineKeyboard(row_width=3)
keyboard.add(
    InlineButton('1', 'inline_keyboard:1'),
    InlineButton('2', 'inline_keyboard:2'),
    InlineButton('3', 'inline_keyboard:3'),
    InlineButton('4', 'inline_keyboard:4'),
    InlineButton('5', 'inline_keyboard:5'),
    InlineButton('6', 'inline_keyboard:6'),
    InlineButton('7', 'inline_keyboard:7')
)
```

##### Row-based Layout

```python
keyboard = InlineKeyboard()
keyboard.row(InlineButton('1', 'inline_keyboard:1'))
keyboard.row(
    InlineButton('2', 'inline_keyboard:2'),
    InlineButton('3', 'inline_keyboard:3')
)
keyboard.row(InlineButton('4', 'inline_keyboard:4'))
keyboard.row(
    InlineButton('5', 'inline_keyboard:5'),
    InlineButton('6', 'inline_keyboard:6')
)
```

#### Pagination

```python
from pykeyboard import InlineKeyboard
```

**Parameters:**
- `count_pages` (int): Total number of pages (≥ 1)
- `current_page` (int): Current page number (≥ 1, ≤ count_pages)
- `callback_pattern` (str): Pattern with `{number}` placeholder

##### Examples

**3 Pages:**
```python
keyboard = InlineKeyboard()
keyboard.paginate(3, 2, 'pagination:{number}')
```

**5 Pages:**
```python
keyboard = InlineKeyboard()
keyboard.paginate(5, 3, 'pagination:{number}')
```

**Large Pagination:**
```python
keyboard = InlineKeyboard()
keyboard.paginate(100, 50, 'page:{number}')
```

**With Additional Buttons:**
```python
keyboard = InlineKeyboard()
keyboard.paginate(150, 75, 'page:{number}')
keyboard.row(
    InlineButton('🔙 Back', 'action:back'),
    InlineButton('❌ Close', 'action:close')
)
```

#### Language Selection

```python
from pykeyboard import InlineKeyboard
```

**Parameters:**
- `callback_pattern` (str): Pattern with `{locale}` placeholder
- `locales` (str | List[str]): Language codes or list of codes
- `row_width` (int, default 2): Buttons per row

**Supported Languages (50+):**
- `en_US` - 🇺🇸 English (US)
- `en_GB` - 🇬🇧 English (UK)
- `es_ES` - 🇪🇸 Español
- `fr_FR` - 🇫🇷 Français
- `de_DE` - 🇩🇪 Deutsch
- `it_IT` - 🇮🇹 Italiano
- `pt_BR` - 🇧🇷 Português (Brasil)
- `ru_RU` - 🇷🇺 Русский
- `zh_CN` - 🇨🇳 中文
- `ja_JP` - 🇯🇵 日本語
- `ko_KR` - 🇰🇷 한국어
- `ar_SA` - 🇸🇦 العربية
- And 40+ more languages...

**Example:**
```python
keyboard = InlineKeyboard(row_width=3)
keyboard.languages(
    'lang:{locale}',
    ['en_US', 'es_ES', 'fr_FR', 'de_DE', 'ru_RU'],
    2
)
```

### Reply Keyboard

```python
from pykeyboard import ReplyKeyboard
```

#### Parameters

- `resize_keyboard` (bool, optional): Whether to resize keyboard
- `one_time_keyboard` (bool, optional): Whether it's one-time
- `selective` (bool, optional): Whether keyboard is selective
- `placeholder` (str, optional): Input field placeholder
- `row_width` (int, default 3): Buttons per row

#### Basic Usage

##### Adding Buttons

```python
from pykeyboard import ReplyKeyboard, ReplyButton

keyboard = ReplyKeyboard(row_width=3, resize_keyboard=True)
keyboard.add(
    ReplyButton('Reply button 1'),
    ReplyButton('Reply button 2'),
    ReplyButton('Reply button 3'),
    ReplyButton('Reply button 4'),
    ReplyButton('Reply button 5')
)
```

##### Row-based Layout

```python
keyboard = ReplyKeyboard(resize_keyboard=True)
keyboard.row(ReplyButton('Reply button 1'))
keyboard.row(
    ReplyButton('Reply button 2'),
    ReplyButton('Reply button 3')
)
keyboard.row(ReplyButton('Reply button 4'))
keyboard.row(ReplyButton('Reply button 5'))
```

##### Advanced Features

```python
keyboard = ReplyKeyboard(
    resize_keyboard=True,
    one_time_keyboard=True,
    placeholder="Choose an option..."
)

keyboard.row(
    ReplyButton("📱 Share Contact", request_contact=True),
    ReplyButton("📍 Share Location", request_location=True)
)
keyboard.row(ReplyButton("❌ Cancel"))
```

## 🔧 Advanced Features

### Type Safety & Validation

PyKeyboard uses Pydantic for comprehensive runtime validation:

```python
# Automatic validation with descriptive errors
try:
    button = InlineButton("", "callback")  # Empty text
except ValueError as e:
    print(f"Validation Error: {e}")

# Full type hints and IDE support
def create_menu() -> InlineKeyboard:
    keyboard: InlineKeyboard = InlineKeyboard()
    button: InlineButton = InlineButton(
        text="Click me!",
        callback_data="action:click"
    )
    keyboard.add(button)
    return keyboard
```

### JSON Serialization

```python
# Serialize to JSON
keyboard = InlineKeyboard()
keyboard.add(InlineButton("Test", "test"))

# Save to file
with open('keyboard.json', 'w') as f:
    f.write(keyboard.model_dump_json())

# Load from file
with open('keyboard.json', 'r') as f:
    data = f.read()
    restored = InlineKeyboard.model_validate_json(data)
```

### Error Handling

PyKeyboard provides comprehensive error handling:

```python
# Pagination validation
try:
    keyboard.paginate(0, 1, "page:{number}")  # Invalid count_pages
except ValueError as e:
    print(f"Pagination error: {e}")

# Language validation
try:
    keyboard.languages("lang:{locale}", [])  # Empty locales
except ValueError as e:
    print(f"Language error: {e}")

# Button validation
try:
    button = InlineButton("", "callback")  # Empty text
except ValueError as e:
    print(f"Button error: {e}")
```

## 🚨 Error Reporting (Non-intrusive, Pretty, Out of the Box)

PyKeyboard provides developer-friendly error reporting that:
- Focuses on user code with trimmed tracebacks
- Offers actionable suggestions and mini examples
- Does not modify global logging or intercept host exceptions

Default behavior
- No configuration is required. Errors raised within pykeyboard APIs are wrapped in PyKeyboardError with a pretty, compact report available via e.get_full_report().
- Logs are emitted via a pykeyboard-bound Loguru logger (record.extra['library'] == 'pykeyboard'). Your application can choose to display or persist them.

Optional: show pykeyboard-only logs in stderr or a file
```python
from pykeyboard import enable_stderr_logging, enable_file_logging, init_logging_from_env

# Option A: enable a filtered stderr sink (pykeyboard-only)
enable_stderr_logging("INFO")  # no global sink removal, no interference

# Option B: enable a filtered file sink (pykeyboard-only)
enable_file_logging("pykeyboard_errors.log")

# Option C: use environment variables and call init helper (pykeyboard-only)
#   export PYKEYBOARD_LOG_LEVEL=INFO
#   export PYKEYBOARD_FILE_LOG_PATH=./pykeyboard_errors.log
init_logging_from_env()
```

Example: automatic reporting, no decorators
```python
from pykeyboard import InlineKeyboard

keyboard = InlineKeyboard()
try:
    keyboard.paginate(0, 1, "page_{number}")  # invalid: count_pages must be >= 1
except Exception as e:
    # Minimal message for user-facing flow
    print(str(e))
    # Full, developer-friendly report with trimmed traceback and suggestions
    if hasattr(e, "get_full_report"):
        print(e.get_full_report())
```

What you get (abridged)
```
🚨 PyKeyboard Error
==================================================
Code: PAGINATION_ERROR
Message: Invalid pagination parameter 'count_pages': count_pages must be >= 1

Location (user code):
  File: example.py:12
  Function: main()
  Code: keyboard.paginate(0, 1, "page_{number}")

Suggestions:
💡 Fix pagination parameters
   1. Check that count_pages >= 1
   2. Ensure current_page is between 1 and count_pages
   3. Verify callback_pattern contains '{number}' placeholder
```

Notes
- No global sys.excepthook is installed by the library.
- No global Loguru sinks are removed or added by default.
- Helper functions are opt-in and filter strictly to pykeyboard logs.

## 📚 API Reference

### InlineKeyboard

| Method | Description | Parameters |
|--------|-------------|------------|
| `add(*buttons)` | Add buttons in rows | `*buttons: InlineButton` |
| `row(*buttons)` | Add single row | `*buttons: InlineButton` |
| `paginate()` | Create pagination | `count_pages, current_page, callback_pattern` |
| `languages()` | Create language selection | `callback_pattern, locales, row_width` |
| `pyrogram_markup` | Get Pyrogram markup | Property |
| `to_dict()` | Serialize to dict | - |
| `from_dict(data)` | Deserialize from dict | `data: Dict[str, Any]` |

### ReplyKeyboard

| Method | Description | Parameters |
|--------|-------------|------------|
| `add(*buttons)` | Add buttons in rows | `*buttons: ReplyButton` |
| `row(*buttons)` | Add single row | `*buttons: ReplyButton` |
| `pyrogram_markup` | Get Pyrogram markup | Property |

### Button Classes

#### InlineButton
- `text: str` - Display text (required, non-empty)
- `callback_data: str | bytes | None` - Callback data
- `url: str | None` - URL to open
- `web_app: WebAppInfo | None` - Web app
- `login_url: LoginUrl | None` - Login URL
- `user_id: int | None` - User ID
- `switch_inline_query: str | None` - Inline query
- `switch_inline_query_current_chat: str | None` - Current chat query
- `callback_game: CallbackGame | None` - Callback game
- `requires_password: bool | None` - Password requirement
- `pay: bool | None` - Pay button
- `copy_text: str | None` - Text to copy

#### ReplyButton
- `text: str` - Display text (required, non-empty)
- `request_contact: bool | None` - Request contact
- `request_location: bool | None` - Request location
- `request_poll: KeyboardButtonPollType | None` - Request poll
- `request_users: KeyboardButtonRequestUsers | None` - Request users
- `request_chat: KeyboardButtonRequestChat | None` - Request chat
- `web_app: WebAppInfo | None` - Web app

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Setting up the development environment
- Code style and standards
- Testing guidelines
- Submitting pull requests

### Community & Support

- 📖 **[Documentation](https://pykeyboard.readthedocs.io/)** - Comprehensive guides and API reference
- 💬 **[GitHub Discussions](https://github.com/johnnie-610/pykeyboard/discussions)** - General questions and community support
- 🐛 **[GitHub Issues](https://github.com/johnnie-610/pykeyboard/issues)** - Bug reports and feature requests
- 🌟 **[Community Guide](COMMUNITY.md)** - Get involved and help improve PyKeyboard
- 📜 **[Code of Conduct](CODE_OF_CONDUCT.md)** - Our community standards and guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/johnnie-610/pykeyboard.git
cd pykeyboard

# Install dependencies
poetry install

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Run with coverage
pytest --cov=pykeyboard --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for [Kurigram](https://github.com/KurimuzonAkuma/pyrogram) - A powerful Pyrogram fork
- Uses [Pydantic](https://pydantic-docs.helpmanual.io/) for type validation
- Inspired by the need for better Telegram bot keyboard libraries

---

<p align="center">Made with ❤️ for the Telegram bot development community</p>

# Installation

```shell

pip install pykeyboard-kurigram

```

or

```shell

poetry add pykeyboard-kurigram

```

# Documentation

## Inline Keyboard

```python
from pykeyboard import InlineKeyboard
```

##### Parameters:

- row_width (integer, default 3)

### Inline Keyboard add buttons

#### Code

```python
from pykeyboard import InlineKeyboard, InlineButton


keyboard = InlineKeyboard(row_width=3)
keyboard.add(
    InlineButton('1', 'inline_keyboard:1'),
    InlineButton('2', 'inline_keyboard:2'),
    InlineButton('3', 'inline_keyboard:3'),
    InlineButton('4', 'inline_keyboard:4'),
    InlineButton('5', 'inline_keyboard:5'),
    InlineButton('6', 'inline_keyboard:6'),
    InlineButton('7', 'inline_keyboard:7')
)
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/add_inline_button.png" alt="add_inline_button"></p>

### Inline Keyboard row buttons

#### Code

```python
from pykeyboard import InlineKeyboard, InlineButton


keyboard = InlineKeyboard()
keyboard.row(InlineButton('1', 'inline_keyboard:1'))
keyboard.row(
    InlineButton('2', 'inline_keyboard:2'),
    InlineButton('3', 'inline_keyboard:3')
)
keyboard.row(InlineButton('4', 'inline_keyboard:4'))
keyboard.row(
    InlineButton('5', 'inline_keyboard:5'),
    InlineButton('6', 'inline_keyboard:6')
)
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/row_inline_button.png" alt="row_inline_button"></p>

### Pagination inline keyboard

```python
from pykeyboard import InlineKeyboard
```

#### Parameters:

- count_pages (integer)
- current_page (integer)
- callback_pattern (string) - use of the `{number}` pattern is <ins>required</ins>

#### Pagination 3 pages

#### Code

```python
from pykeyboard import InlineKeyboard

keyboard = InlineKeyboard()
keyboard.paginate(3, 3, 'pagination_keyboard:{number}')
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_3.png" alt="pagination_keyboard_3"></p>

#### Pagination 5 pages

#### Code

```python
from pykeyboard import InlineKeyboard

keyboard = InlineKeyboard()
keyboard.paginate(5, 3, 'pagination_keyboard:{number}')
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_5.png" alt="pagination_keyboard_5"></p>

#### Pagination 9 pages

#### Code

```python
from pykeyboard import InlineKeyboard

keyboard = InlineKeyboard()
keyboard.paginate(9, 5, 'pagination_keyboard:{number}')
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_9.png" alt="pagination_keyboard_9"></p>

#### Pagination 100 pages

#### Code

```python
from pykeyboard import InlineKeyboard

keyboard = InlineKeyboard()
keyboard.paginate(100, 100, 'pagination_keyboard:{number}')
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_100.png" alt="pagination_keyboard_100"></p>

#### Pagination 150 pages and buttons

#### Code

```python
from pykeyboard import InlineKeyboard, InlineButton

keyboard = InlineKeyboard()
keyboard.paginate(150, 123, 'pagination_keyboard:{number}')
keyboard.row(
    InlineButton('Back', 'pagination_keyboard:back'),
    InlineButton('Close', 'pagination_keyboard:close')
)
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_150.png" alt="pagination_keyboard_150"></p>

### Languages inline keyboard

```python
from pykeyboard import InlineKeyboard
```

#### Parameters:

- callback_pattern (string) - use of the `{locale}` pattern is <ins>required</ins>
- locales (string | list) - list of language codes
  - be_BY - Belarusian
  - de_DE - German
  - zh_CN - Chinese
  - en_US - English
  - fr_FR - French
  - id_ID - Indonesian
  - it_IT - Italian
  - ko_KR - Korean
  - tr_TR - Turkish
  - ru_RU - Russian
  - es_ES - Spanish
  - uk_UA - Ukrainian
  - uz_UZ - Uzbek
- row_width (integer, default 2)


#### Code

```python
from pykeyboard import InlineKeyboard


keyboard = InlineKeyboard(row_width=3)
keyboard.languages(
    'languages:{locale}', ['en_US', 'ru_RU', 'id_ID'], 2
)
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/languages_keyboard.png" alt="languages_keyboard"></p>

## Reply Keyboard

```python
from pykeyboard import ReplyKeyboard
```

#### Parameters:

- resize_keyboard (bool, optional)
- one_time_keyboard (bool, optional)
- selective (bool, optional)
- row_width (integer, default 3)

### Reply Keyboard add buttons

#### Code

```python
from pykeyboard import ReplyKeyboard, ReplyButton


keyboard = ReplyKeyboard(row_width=3)
keyboard.add(
    ReplyButton('Reply button 1'),
    ReplyButton('Reply button 2'),
    ReplyButton('Reply button 3'),
    ReplyButton('Reply button 4'),
    ReplyButton('Reply button 5')
)
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/add_reply_button.png" alt="add_reply_button"></p>

### Reply Keyboard row buttons

#### Code

```python
from pykeyboard import ReplyKeyboard, ReplyButton


keyboard = ReplyKeyboard()
keyboard.row(ReplyButton('Reply button 1'))
keyboard.row(
    ReplyButton('Reply button 2'),
    ReplyButton('Reply button 3')
)
keyboard.row(ReplyButton('Reply button 4'))
keyboard.row(ReplyButton('Reply button 5'))
```

#### Result

<p><img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/row_reply_button.png" alt="row_reply_button"></p>
