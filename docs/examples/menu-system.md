# Menu System Example

This example demonstrates how to create a hierarchical menu system using PyKeyboard with navigation between different menu levels.

<strong><em>Note: ALTHOUGH WE BELIEVE THIS EXAMPLE SHOULD WORK, IT IS NOT TESTED AND MIGHT NOT WORK. </em></strong>
<strong><em>USE AT YOUR OWN RISK. YOU CAN INSTEAD REFER TO THIS SCRIPT WHICH HAS BEEN TESTED AND WORKS: <a href="https://github.com/johnnie-610/pykeyboard/blob/main/showcase_bot.py">Showcase Bot</a>.</em></strong>

## Overview

This example shows:
- Creating multi-level menu systems
- Navigation between menus
- State management for menu context
- Using the KeyboardBuilder for complex layouts

## Code Example

```python
from pyrogram import Client, filters
from pykeyboard import KeyboardBuilder, InlineKeyboard
from typing import Dict

app = Client("menu_bot")

# Menu state storage (in production, use a database)
user_menu_states: Dict[int, str] = {}

# Define menu structure
MAIN_MENU = "main"
SETTINGS_MENU = "settings"
PROFILE_MENU = "profile"

def create_main_menu():
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("📊 Dashboard", callback_data="menu:dashboard"),
        InlineButton("⚙️ Settings", callback_data="menu:settings"),
        InlineButton("👤 Profile", callback_data="menu:profile"),
        InlineButton("ℹ️ Help", callback_data="menu:help")
    )
    return keyboard

def create_settings_menu():
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("🔔 Notifications", callback_data="settings:notifications"),
        InlineButton("🌐 Language", callback_data="settings:language"),
        InlineButton("🔒 Privacy", callback_data="settings:privacy"),
        InlineButton("⬅️ Back", callback_data="menu:main")
    )
    return keyboard

def create_profile_menu():
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("📝 Edit Profile", callback_data="profile:edit"),
        InlineButton("📸 Change Photo", callback_data="profile:photo"),
        InlineButton("📊 Statistics", callback_data="profile:stats"),
        InlineButton("⬅️ Back", callback_data="menu:main")
    )
    return keyboard

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    user_menu_states[user_id] = MAIN_MENU

    keyboard = create_main_menu()
    await message.reply_text(
        "🏠 **Main Menu**\n\nWelcome! Choose an option:",
        reply_markup=keyboard.pyrogram_markup
    )

@app.on_callback_query(filters.regex(r"^menu:"))
async def handle_menu_navigation(client, callback_query):
    user_id = callback_query.from_user.id
    menu_action = callback_query.data.split(":", 1)[1]

    if menu_action == "main":
        user_menu_states[user_id] = MAIN_MENU
        keyboard = create_main_menu()
        await callback_query.edit_message_text(
            "🏠 **Main Menu**\n\nChoose an option:",
            reply_markup=keyboard.pyrogram_markup
        )

    elif menu_action == "settings":
        user_menu_states[user_id] = SETTINGS_MENU
        keyboard = create_settings_menu()
        await callback_query.edit_message_text(
            "⚙️ **Settings**\n\nConfigure your preferences:",
            reply_markup=keyboard.pyrogram_markup
        )

    elif menu_action == "profile":
        user_menu_states[user_id] = PROFILE_MENU
        keyboard = create_profile_menu()
        await callback_query.edit_message_text(
            "👤 **Profile**\n\nManage your profile:",
            reply_markup=keyboard.pyrogram_markup
        )

    elif menu_action == "help":
        await callback_query.edit_message_text(
            "ℹ️ **Help**\n\n"
            "• Dashboard: View your statistics\n"
            "• Settings: Configure preferences\n"
            "• Profile: Manage your account\n\n"
            "Use the Back buttons to navigate.",
            reply_markup=create_main_menu().pyrogram_markup
        )

    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^(settings|profile):"))
async def handle_submenu_actions(client, callback_query):
    action = callback_query.data

    if action == "settings:notifications":
        await callback_query.answer("Notifications settings opened!")
        # Implement notifications settings

    elif action == "settings:language":
        await callback_query.answer("Language settings opened!")
        # Implement language selection

    elif action == "profile:edit":
        await callback_query.answer("Profile editing opened!")
        # Implement profile editing

    # Add more submenu handlers as needed

if __name__ == "__main__":
    app.run()
```

## Features Demonstrated

- Hierarchical menu navigation
- State management for user context
- Callback data routing
- Dynamic keyboard generation
- Back navigation

## Menu Structure

```
Main Menu
├── Dashboard
├── Settings
│   ├── Notifications
│   ├── Language
│   └── Privacy
├── Profile
│   ├── Edit Profile
│   ├── Change Photo
│   └── Statistics
└── Help
```

## Running the Example

1. Install PyKeyboard: `pip install pykeyboard-kurigram`
2. Set up your bot token
3. Run the script: `python menu_system.py`
4. Send `/start` to see the main menu
5. Navigate through different menu levels