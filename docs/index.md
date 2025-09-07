# PyKeyboard Documentation

<div align="center">
<p align="center">
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/logo.png" alt="pykeyboard">
</p>

**Best Keyboard Library for Kurigram**

</div>

## 🚀 What is PyKeyboard?

PyKeyboard is a modern, fully type-safe Python library for creating beautiful and functional inline and reply keyboards for Telegram bots using [Kurigram](https://pypi.org/project/kurigram).

### ✨ Key Features


- 🌍 **50+ Languages** - Comprehensive locale support with native language names and flags
- 📖 **Pagination** - Advanced pagination with automatic duplicate prevention
- 🌐 **Language Selection** - Built-in multi-language keyboard support

## 📖 Quick Examples

### Inline Keyboard
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

### Reply Keyboard
```python
from pykeyboard import ReplyKeyboard, ReplyButton

# Create a reply keyboard
keyboard = ReplyKeyboard(resize_keyboard=True, one_time_keyboard=True)
keyboard.add(
    ReplyButton("Yes"),
    ReplyButton("No"),
    ReplyButton("Maybe")
)

# Use with Kurigram
await message.reply_text("Choose an option:", reply_markup=keyboard)
```

## 🎯 Perfect For

- **Telegram Bot Developers** - Create beautiful, functional keyboards with ease
- **E-commerce Bots** - Product catalogs with pagination and search
- **Menu-driven Interfaces** - Complex navigation systems
- **Multi-language Applications** - Built-in language selection
- **Form Handling** - User input collection with reply keyboards
- **Interactive Applications** - Any bot requiring user interaction

## 🏗️ Architecture

PyKeyboard provides a clean, modular architecture:

- **Core Classes**: `InlineKeyboard`, `ReplyKeyboard`, `InlineButton`, `ReplyButton`
- **Builder Pattern**: `KeyboardBuilder` for fluent API construction
- **Factory Pattern**: `KeyboardFactory` for common keyboard templates
- **Localization**: 50+ language support with automatic detection


## 🤝 Community & Support

- 📖 **[GitHub Repository](https://github.com/johnnie-610/pykeyboard)** - Source code and issues
- 💬 **[GitHub Discussions](https://github.com/johnnie-610/pykeyboard/discussions)** - Community support
- 🐛 **[Issue Tracker](https://github.com/johnnie-610/pykeyboard/issues)** - Bug reports and feature requests


## 📄 License

This project is licensed under the MIT License - see the <a href="https://github.com/johnnie-610/pykeyboard/blob/main/LICENSE">LICENSE</a> for details.

---

<div align="center">
<strong><em>Made with ❤️ for the Telegram bot development community</em></strong>
</div>