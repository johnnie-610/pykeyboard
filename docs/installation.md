# Installation

PyKeyboard is available on PyPI and can be installed using pip or poetry.

## Requirements

- Python 3.9 or higher
- [Kurigram](https://pypi.org/project/kurigram) (automatically installed)

## Install with pip

```bash
pip install pykeyboard-kurigram
```

## Install with poetry

```bash
poetry add pykeyboard-kurigram
```

## Install from source

```bash
git clone https://github.com/johnnie-610/pykeyboard.git
cd pykeyboard
pip install -e .
```

## Development Setup

For development and testing:

```bash
git clone https://github.com/johnnie-610/pykeyboard.git
cd pykeyboard
poetry install
```

## Dependencies

PyKeyboard has minimal dependencies:

- `pydantic >= 2.11.7` - Type validation
- `kurigram >= 2.2.10` - Telegram bot framework

Optional dependencies:

- `TgCrypto` - Faster Pyrogram performance (recommended)

## Verification

After installation, verify PyKeyboard is working:

```python
import pykeyboard

# Check version
print(pykeyboard.__version__)

# Quick test
from pykeyboard import InlineKeyboard, InlineButton

keyboard = InlineKeyboard()
keyboard.add(InlineButton("Test", "test"))
print("✅ PyKeyboard is working!")
```

## Troubleshooting

### Import Error

If you get import errors, make sure you're using Python 3.9+:

```bash
python --version
```

### Kurigram Issues

PyKeyboard requires Kurigram. If you have import issues:

```bash
pip install kurigram
```

### TgCrypto Warning

You might see a warning about TgCrypto missing. This is optional but recommended:

```bash
pip install TgCrypto
```

This will improve Pyrogram's performance but is not required for PyKeyboard to work.
