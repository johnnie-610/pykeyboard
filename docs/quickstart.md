# Quick Start

Get up and running with PyKeyboard in 5 minutes.

## Basic Setup

First, install PyKeyboard:

```bash
pip install pykeyboard-kurigram
```

## Your First Keyboard

```python
from pykeyboard import InlineKeyboard, InlineButton

# Create a keyboard
keyboard = InlineKeyboard()
keyboard.add(
    InlineButton("👍 Like", "action:like"),
    InlineButton("👎 Dislike", "action:dislike"),
    InlineButton("📊 Stats", "action:stats")
)

# Use with Kurigram
await message.reply_text("What do you think?", reply_markup=keyboard)
```

## Handling Callbacks

```python
from pyrogram import Client, filters

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_callback_query(filters.regex("action:like"))
async def handle_like(client, callback_query):
    await callback_query.answer("You liked it! 👍")
    # Update your database, etc.

@app.on_callback_query(filters.regex("action:dislike"))
async def handle_dislike(client, callback_query):
    await callback_query.answer("You disliked it! 👎")

@app.on_callback_query(filters.regex("action:stats"))
async def handle_stats(client, callback_query):
    stats = get_stats()  # Your stats function
    await callback_query.edit_message_text(f"📊 Stats: {stats}")
```

## Reply Keyboards

```python
from pykeyboard import ReplyKeyboard, ReplyButton

# Create a reply keyboard
keyboard = ReplyKeyboard(resize_keyboard=True, one_time_keyboard=True)
keyboard.add(
    ReplyButton("📱 Share Phone", request_contact=True),
    ReplyButton("📍 Share Location", request_location=True),
    ReplyButton("❌ Cancel")
)

await message.reply_text("Please share your contact:", reply_markup=keyboard)
```

## Advanced Features

### Pagination

```python
keyboard = InlineKeyboard()
keyboard.paginate(
    count_pages=10,
    current_page=1,
    callback_pattern="page:{number}"
)
```

### Language Selection

```python
keyboard = InlineKeyboard()
keyboard.languages(
    callback_pattern="lang:{locale}",
    locales=["en_US", "es_ES", "fr_FR"]
)
```

### Builder Pattern

```python
from pykeyboard import KeyboardBuilder

builder = KeyboardBuilder(InlineKeyboard())
keyboard = (builder
    .add_button("Yes", "yes")
    .add_button("No", "no")
    .add_row("Maybe", "cancel")
    .build())
```

## Complete Example

```python
from pyrogram import Client, filters
from pykeyboard import InlineKeyboard, InlineButton

# Bot setup
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("🎮 Play Game", "game"),
        InlineButton("ℹ️ About", "about"),
        InlineButton("⚙️ Settings", "settings")
    )

    await message.reply_text(
        "Welcome to My Bot! Choose an option:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("game"))
async def game_callback(client, callback_query):
    await callback_query.edit_message_text("🎮 Game starting...")

@app.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query):
    await callback_query.edit_message_text("ℹ️ This is a demo bot using PyKeyboard!")

@app.on_callback_query(filters.regex("settings"))
async def settings_callback(client, callback_query):
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("🌐 Language", "lang"),
        InlineButton("🔔 Notifications", "notif"),
        InlineButton("⬅️ Back", "back")
    )

    await callback_query.edit_message_text(
        "⚙️ Settings:",
        reply_markup=keyboard
    )

if __name__ == "__main__":
    app.run()
```

## Next Steps

- Check out the [examples](../examples/basic-bot) for more advanced usage
- Read the [API documentation](../api/inline-keyboard) for detailed reference
- Explore [pagination](../inline-keyboards#pagination) and [language selection](../inline-keyboards#language-selection) features
- Join our [GitHub Discussions](https://github.com/johnnie-610/pykeyboard/discussions) for community support