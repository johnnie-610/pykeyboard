# Basic Bot Example

This example demonstrates how to create a simple Telegram bot using PyKeyboard for basic keyboard interactions.

<strong><em>Note: ALTHOUGH WE BELIEVE THIS EXAMPLE SHOULD WORK, IT IS NOT TESTED AND MIGHT NOT WORK. </em></strong>
<strong><em>USE AT YOUR OWN RISK. YOU CAN INSTEAD REFER TO THIS SCRIPT WHICH HAS BEEN TESTED AND WORKS: <a href="https://github.com/johnnie-610/pykeyboard/blob/main/showcase_bot.py">Showcase Bot</a>.</em></strong>

## Overview

This example shows:
- Creating a basic inline keyboard
- Handling callback queries
- Simple bot structure

## Code Example

```python
from pyrogram import Client, filters
from pykeyboard import InlineKeyboard, InlineButton

app = Client("basic_bot")

# Create a simple keyboard
keyboard = InlineKeyboard()
keyboard.add(
    InlineButton("Option 1", callback_data="option1"),
    InlineButton("Option 2", callback_data="option2"),
    InlineButton("Help", callback_data="help")
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Choose an option:",
        reply_markup=keyboard.pyrogram_markup
    )

@app.on_callback_query()
async def handle_callback(client, callback_query):
    data = callback_query.data

    if data == "option1":
        await callback_query.answer("You selected Option 1!")
        await callback_query.edit_message_text("You chose Option 1")
    elif data == "option2":
        await callback_query.answer("You selected Option 2!")
        await callback_query.edit_message_text("You chose Option 2")
    elif data == "help":
        await callback_query.answer("Help information")
        await callback_query.edit_message_text(
            "This is a basic bot example.\n\n"
            "Use /start to see the keyboard again."
        )

if __name__ == "__main__":
    app.run()
```

## Features Demonstrated

- Basic inline keyboard creation
- Callback query handling
- Message editing
- Simple command handling

## Running the Example

1. Install PyKeyboard: `pip install pykeyboard-kurigram`
2. Set up your bot token in environment variables
3. Run the script: `python basic_bot.py`
4. Send `/start` to your bot to see the keyboard