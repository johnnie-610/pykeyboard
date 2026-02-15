<div align="center">
<p align="center">
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/logo.png" alt="pykeyboard">
</p>

![PyPI](https://img.shields.io/pypi/v/pykeyboard-kurigram)
[![Downloads](https://pepy.tech/badge/pykeyboard-kurigram)](https://pepy.tech/project/pykeyboard-kurigram)
![Python Version](https://img.shields.io/pypi/pyversions/pykeyboard-kurigram)
![License](https://img.shields.io/github/license/johnnie-610/pykeyboard)

</div>

# PyKeyboard

**Best Keyboard Library for Kurigram**

PyKeyboard is a comprehensive Python library for creating beautiful and functional inline and reply keyboards for Telegram bots using [Kurigram](https://pypi.org/project/kurigram).

## Features

- 🎯 **Inline & Reply Keyboards** — full Pyrogram-compatible button types (URL, callback, contact, location, web app, etc.)
- 📄 **Pagination** — automatic page navigation with duplicate-prevention and LRU caching
- 🌍 **50+ Languages** — built-in locale support with native names, flags, and custom locale registration
- 🏗️ **Builder Pattern** — fluent `KeyboardBuilder` API with method chaining for complex layouts
- 🏭 **Factory Presets** — `KeyboardFactory` for one-line confirmation, menu, rating, pagination, and language keyboards
- 🪝 **Hooks & Validation** — `ButtonValidator` and `KeyboardHookManager` for rule-based button validation and transforms
- 🚨 **Structured Errors** — typed error classes with `error_code`, `param`, `value`, and `reason` attributes

## Installation

```bash
# Using pip
pip install pykeyboard-kurigram

# Using poetry
poetry add pykeyboard-kurigram

# Using uv
uv add pykeyboard-kurigram
```

## Quick Start

### Inline Keyboard

```python
from pykeyboard import InlineKeyboard, InlineButton

keyboard = InlineKeyboard()
keyboard.add(
    InlineButton("👍 Like", "action:like"),
    InlineButton("👎 Dislike", "action:dislike"),
    InlineButton("📊 Stats", "action:stats")
)

await message.reply_text("What do you think?", reply_markup=keyboard)
```

### Builder Pattern

```python
from pykeyboard import KeyboardBuilder, InlineKeyboard

kb = (
    KeyboardBuilder(InlineKeyboard())
    .add_row("🏠 Home", "⚙️ Settings")
    .add_row("📊 Stats", "🆘 Help")
    .add_navigation_buttons(10, 5, "page_{number}")
    .build()
)
```

### Error Handling

```python
from pykeyboard import InlineKeyboard, PyKeyboardError

try:
    kb = InlineKeyboard(row_width=0)
except PyKeyboardError as e:
    print(e.error_code)  # "CONFIGURATION_ERROR"
    print(e.param)       # "row_width"
    print(e.value)       # 0
```

## Showcase Bot

A fully tested showcase bot demonstrating every feature is included in the repository:

```bash
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_API_ID="..."
export TELEGRAM_API_HASH="..."
python showcase_bot.py
```

See [showcase_bot.py](showcase_bot.py) for the complete source.

## Documentation

For comprehensive documentation, see the [docs](https://johnnie-610.github.io/pykeyboard/) or check the `showcase_bot.py` file for sequential usage examples.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ for the Telegram bot development community</p>
