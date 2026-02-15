# Basic Bot Example

A minimal bot demonstrating inline keyboard creation and callback handling.

!!! tip "Tested Reference"
For a fully tested, comprehensive example, see the [Showcase Bot](showcase-bot.md).

## Overview

This example shows:

- Creating a basic inline keyboard
- Handling callback queries
- Error handling with `PyKeyboardError`

## Code

```python
from pyrogram import Client, filters
from pykeyboard import InlineKeyboard, InlineButton, PyKeyboardError

app = Client("basic_bot")


def main_keyboard():
    """Create the main menu keyboard."""
    keyboard = InlineKeyboard(row_width=3)
    keyboard.add(
        InlineButton("Option 1", callback_data="option1"),
        InlineButton("Option 2", callback_data="option2"),
        InlineButton("Help", callback_data="help"),
    )
    return keyboard


@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Choose an option:",
        reply_markup=main_keyboard(),
    )


@app.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data

    try:
        match data:
            case "option1":
                await callback_query.answer("You selected Option 1!")
                await callback_query.edit_message_text(
                    "You chose Option 1",
                    reply_markup=main_keyboard(),
                )
            case "option2":
                await callback_query.answer("You selected Option 2!")
                await callback_query.edit_message_text(
                    "You chose Option 2",
                    reply_markup=main_keyboard(),
                )
            case "help":
                await callback_query.edit_message_text(
                    "ℹ️ **Help**\n\n"
                    "• Option 1/2: Demo callback responses\n"
                    "• Use /start to reset the keyboard",
                    reply_markup=main_keyboard(),
                )
            case _:
                await callback_query.answer(f"Unknown: {data}")
    except PyKeyboardError as e:
        await callback_query.answer(f"Error: {e.error_code}")


if __name__ == "__main__":
    app.run()
```

## Features Demonstrated

- Inline keyboard creation with `InlineKeyboard` and `InlineButton`
- Callback query routing with `match/case`
- Error handling with `PyKeyboardError`
- Keyboard re-display after each action

## Running

```bash
pip install pykeyboard-kurigram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_API_ID="..."
export TELEGRAM_API_HASH="..."
python basic_bot.py
```

Send `/start` to see the keyboard.
