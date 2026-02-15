# Menu System Example

A hierarchical menu bot demonstrating navigation between different menu levels using `KeyboardBuilder`.

!!! tip "Tested Reference"
For a fully tested, comprehensive example, see the [Showcase Bot](showcase-bot.md).

## Overview

This example shows:

- Creating multi-level menu systems
- Navigation between menus with back buttons
- Using `KeyboardBuilder` for fluent keyboard construction
- State management for menu context

## Code

```python
from pyrogram import Client, filters
from pykeyboard import KeyboardBuilder, InlineKeyboard, InlineButton, PyKeyboardError

app = Client("menu_bot")

# Menu state storage (in production, use a database)
user_menu_states: dict[int, str] = {}


def create_main_menu() -> InlineKeyboard:
    return (
        KeyboardBuilder(InlineKeyboard(row_width=2))
        .add_row("📊 Dashboard", "⚙️ Settings")
        .add_row("👤 Profile", "ℹ️ Help")
        .build()
    )


def create_settings_menu() -> InlineKeyboard:
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(
        InlineButton("🔔 Notifications", callback_data="settings:notifications"),
        InlineButton("🌐 Language", callback_data="settings:language"),
        InlineButton("🔒 Privacy", callback_data="settings:privacy"),
        InlineButton("⬅️ Back", callback_data="menu:main"),
    )
    return keyboard


def create_profile_menu() -> InlineKeyboard:
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(
        InlineButton("📝 Edit Profile", callback_data="profile:edit"),
        InlineButton("📸 Change Photo", callback_data="profile:photo"),
        InlineButton("📊 Statistics", callback_data="profile:stats"),
        InlineButton("⬅️ Back", callback_data="menu:main"),
    )
    return keyboard


MENUS = {
    "main": ("🏠 **Main Menu**\n\nChoose an option:", create_main_menu),
    "settings": ("⚙️ **Settings**\n\nConfigure your preferences:", create_settings_menu),
    "profile": ("👤 **Profile**\n\nManage your profile:", create_profile_menu),
}


@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_menu_states[message.from_user.id] = "main"
    await message.reply_text(
        "🏠 **Main Menu**\n\nWelcome! Choose an option:",
        reply_markup=create_main_menu(),
    )


@app.on_callback_query(filters.regex(r"^menu:"))
async def handle_menu_navigation(client, callback_query):
    user_id = callback_query.from_user.id
    menu_action = callback_query.data.split(":", 1)[1]

    try:
        if menu_action == "help":
            await callback_query.edit_message_text(
                "ℹ️ **Help**\n\n"
                "• Dashboard: View your statistics\n"
                "• Settings: Configure preferences\n"
                "• Profile: Manage your account\n\n"
                "Use the Back buttons to navigate.",
                reply_markup=create_main_menu(),
            )
        elif menu_action == "dashboard":
            await callback_query.edit_message_text(
                "📊 **Dashboard**\n\nYour stats will appear here.",
                reply_markup=create_main_menu(),
            )
        elif menu_action in MENUS:
            text, factory = MENUS[menu_action]
            user_menu_states[user_id] = menu_action
            await callback_query.edit_message_text(text, reply_markup=factory())
        else:
            await callback_query.answer(f"Unknown menu: {menu_action}")
    except PyKeyboardError as e:
        await callback_query.answer(f"Error: {e.error_code}")

    await callback_query.answer()


@app.on_callback_query(filters.regex(r"^(settings|profile):"))
async def handle_submenu_actions(client, callback_query):
    section, action = callback_query.data.split(":", 1)
    await callback_query.answer(f"{section.title()} → {action} opened!")


if __name__ == "__main__":
    app.run()
```

## Menu Structure

```
Main Menu
├── 📊 Dashboard
├── ⚙️ Settings
│   ├── 🔔 Notifications
│   ├── 🌐 Language
│   └── 🔒 Privacy
├── 👤 Profile
│   ├── 📝 Edit Profile
│   ├── 📸 Change Photo
│   └── 📊 Statistics
└── ℹ️ Help
```

## Features Demonstrated

- `KeyboardBuilder` fluent API for main menu
- `InlineKeyboard.add()` for sub-menus with back buttons
- Menu routing via `match` on callback data sections
- `MENUS` lookup dict to reduce repetition
- `PyKeyboardError` handling

## Running

```bash
pip install pykeyboard-kurigram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_API_ID="..."
export TELEGRAM_API_HASH="..."
python menu_system.py
```

Send `/start` to see the main menu. Navigate through different levels.
