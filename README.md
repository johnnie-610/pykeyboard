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

**Modern, Type-Safe Keyboard Library for Kurigram**

PyKeyboard is a comprehensive Python library for creating beautiful and functional inline and reply keyboards for Telegram bots using [Kurigram](https://github.com/KurimuzonAkuma/pyrogram).

## Installation

```bash
# Using pip
pip install pykeyboard-kurigram

# Using poetry
poetry add pykeyboard-kurigram
```

## Quick Start

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

## Features

- 🎯 **Full Type Safety** - Built with Pydantic v2 for runtime validation
- 🌍 **50+ Languages** - Comprehensive locale support with native language names and flags
- 🧪 **100% Test Coverage** - Extensive test suite with pytest
- 📦 **JSON Serialization** - Built-in keyboard serialization/deserialization
- 🚀 **Modern Python** - Uses latest Python features and best practices
- 🎨 **Beautiful API** - Intuitive, chainable methods for keyboard construction
- 🛡️ **Error Handling** - Comprehensive validation with descriptive error messages

## Documentation

For comprehensive documentation, see the [MkDocs site](https://pykeyboard.readthedocs.io/) or check the `examples.py` file for sequential usage examples.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ for the Telegram bot development community</p>