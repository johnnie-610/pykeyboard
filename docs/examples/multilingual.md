# Multi-language Bot Example

A multilingual bot with language selection, custom locales, and dynamic content translation using PyKeyboard's built-in language support.

!!! tip "Tested Reference"
For a fully tested, comprehensive example, see the [Showcase Bot](showcase-bot.md).

## Overview

This example shows:

- Language selection using built-in locales via `languages()`
- Custom locale registration with `add_custom_locale()`
- Dynamic content translation
- Persistent language preferences

## Code

```python
from pyrogram import Client, filters
from pykeyboard import InlineKeyboard, InlineButton

app = Client("multilingual_bot")

# Language storage (in production, use a database)
user_languages: dict[int, str] = {}

# Translation dictionaries
TRANSLATIONS: dict[str, dict[str, str]] = {
    "en_US": {
        "welcome": "🏠 **Welcome!**\n\nChoose your language:",
        "main_menu": "🏠 **Main Menu**\n\nWhat would you like to do?",
        "settings": "⚙️ **Settings**",
        "language": "🌐 **Language**\n\nSelect your preferred language:",
        "help": "ℹ️ **Help**\n\n/start — Start the bot\n/lang — Change language",
        "dashboard": "📊 **Dashboard**\n\nWelcome back!",
        "change_language": "🌐 Change Language",
        "back": "⬅️ Back",
    },
    "es_ES": {
        "welcome": "🏠 **¡Bienvenido!**\n\nElige tu idioma:",
        "main_menu": "🏠 **Menú Principal**\n\n¿Qué te gustaría hacer?",
        "settings": "⚙️ **Configuración**",
        "language": "🌐 **Idioma**\n\nSelecciona tu idioma preferido:",
        "help": "ℹ️ **Ayuda**\n\n/start — Iniciar el bot\n/lang — Cambiar idioma",
        "dashboard": "📊 **Panel**\n\n¡Bienvenido de vuelta!",
        "change_language": "🌐 Cambiar Idioma",
        "back": "⬅️ Atrás",
    },
    "fr_FR": {
        "welcome": "🏠 **Bienvenue !**\n\nChoisissez votre langue :",
        "main_menu": "🏠 **Menu Principal**\n\nQue souhaitez-vous faire ?",
        "settings": "⚙️ **Paramètres**",
        "language": "🌐 **Langue**\n\nSélectionnez votre langue :",
        "help": "ℹ️ **Aide**\n\n/start — Démarrer le bot\n/lang — Changer de langue",
        "dashboard": "📊 **Tableau de Bord**\n\nBienvenue !",
        "change_language": "🌐 Changer de Langue",
        "back": "⬅️ Retour",
    },
    "de_DE": {
        "welcome": "🏠 **Willkommen!**\n\nWählen Sie Ihre Sprache:",
        "main_menu": "🏠 **Hauptmenü**\n\nWas möchten Sie tun?",
        "settings": "⚙️ **Einstellungen**",
        "language": "🌐 **Sprache**\n\nWählen Sie Ihre bevorzugte Sprache:",
        "help": "ℹ️ **Hilfe**\n\n/start — Bot starten\n/lang — Sprache ändern",
        "dashboard": "📊 **Dashboard**\n\nWillkommen zurück!",
        "change_language": "🌐 Sprache Ändern",
        "back": "⬅️ Zurück",
    },
}

SUPPORTED_LOCALES = ["en_US", "es_ES", "fr_FR", "de_DE"]


def t(user_id: int, key: str) -> str:
    """Translate a key for the user's language."""
    lang = user_languages.get(user_id, "en_US")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en_US"]).get(key, f"[{key}]")


def create_language_keyboard() -> InlineKeyboard:
    """Create language selection keyboard using built-in locales."""
    keyboard = InlineKeyboard()
    keyboard.languages("set_lang:{locale}", SUPPORTED_LOCALES)
    return keyboard


def create_main_menu(user_id: int) -> InlineKeyboard:
    """Create main menu keyboard in user's language."""
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        InlineButton("📊 " + t(user_id, "dashboard").split("\n")[0].strip("* "),
                      callback_data="menu:dashboard"),
        InlineButton("⚙️ " + t(user_id, "settings").split("\n")[0].strip("* "),
                      callback_data="menu:settings"),
        InlineButton("ℹ️ " + t(user_id, "help").split("\n")[0].strip("* "),
                      callback_data="menu:help"),
    )
    return keyboard


@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id

    if user_id not in user_languages:
        # First visit — show language selection
        await message.reply_text(
            t(user_id, "welcome"),
            reply_markup=create_language_keyboard(),
        )
    else:
        await message.reply_text(
            t(user_id, "main_menu"),
            reply_markup=create_main_menu(user_id),
        )


@app.on_callback_query(filters.regex(r"^set_lang:"))
async def handle_language_selection(client, callback_query):
    user_id = callback_query.from_user.id
    locale = callback_query.data.split(":")[1]

    user_languages[user_id] = locale

    await callback_query.edit_message_text(
        t(user_id, "main_menu"),
        reply_markup=create_main_menu(user_id),
    )
    await callback_query.answer(f"Language set to {locale[:2].upper()}!")


@app.on_callback_query(filters.regex(r"^menu:"))
async def handle_menu(client, callback_query):
    user_id = callback_query.from_user.id
    action = callback_query.data.split(":")[1]

    match action:
        case "main":
            text = t(user_id, "main_menu")
            keyboard = create_main_menu(user_id)
        case "settings":
            text = t(user_id, "settings")
            lang = user_languages.get(user_id, "en_US")[:2].upper()
            keyboard = InlineKeyboard(row_width=1)
            keyboard.add(
                InlineButton(
                    f"{t(user_id, 'change_language')} ({lang})",
                    callback_data="settings:language",
                ),
                InlineButton(t(user_id, "back"), callback_data="menu:main"),
            )
        case "dashboard":
            text = t(user_id, "dashboard")
            keyboard = create_main_menu(user_id)
        case "help":
            text = t(user_id, "help")
            keyboard = create_main_menu(user_id)
        case _:
            await callback_query.answer(f"Unknown: {action}")
            return

    await callback_query.edit_message_text(text, reply_markup=keyboard)
    await callback_query.answer()


@app.on_callback_query(filters.regex(r"^settings:language$"))
async def handle_change_language(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.edit_message_text(
        t(user_id, "language"),
        reply_markup=create_language_keyboard(),
    )
    await callback_query.answer()


@app.on_message(filters.command("lang"))
async def change_language_command(client, message):
    """Allow users to change language via /lang command."""
    await message.reply_text(
        t(message.from_user.id, "welcome"),
        reply_markup=create_language_keyboard(),
    )


if __name__ == "__main__":
    app.run()
```

## Adding Custom Locales

You can register custom locales that appear alongside built-in ones:

```python
keyboard = InlineKeyboard()
keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
keyboard.languages("set_lang:{locale}", ["en_US", "en_PIRATE"])
```

## Supported Languages

PyKeyboard supports **50+ built-in locales** with native names and flag emojis. This example uses 4 of them, but you can pass any locale codes to `languages()`.

## Running

```bash
pip install pykeyboard-kurigram
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_API_ID="..."
export TELEGRAM_API_HASH="..."
python multilingual_bot.py
```

Send `/start` to select your language. Use `/lang` to change it later.
