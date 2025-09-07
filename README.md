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

PyKeyboard is a comprehensive Python library for creating beautiful and functional inline and reply keyboards for Telegram bots using [Kurigram](https://pypi.org/project/kurigram).

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
await message.reply_text("What do you think?", reply_markup=keyboard)
```

## Documentation

For comprehensive documentation, see the [docs](https://johnnie-610.github.io/pykeyboard/) or check the `examples.py` file for sequential usage examples.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ for the Telegram bot development community</p>