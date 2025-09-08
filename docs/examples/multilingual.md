# Multi-language Bot Example

This example demonstrates how to create a multilingual bot with language selection, locale management, and translated content using PyKeyboard's built-in language support.

<strong><em>Note: ALTHOUGH WE BELIEVE THIS EXAMPLE SHOULD WORK, IT IS NOT TESTED AND MIGHT NOT WORK. </em></strong>
<strong><em>USE AT YOUR OWN RISK. YOU CAN INSTEAD REFER TO THIS SCRIPT WHICH HAS BEEN TESTED AND WORKS: <a href="https://github.com/johnnie-610/pykeyboard/blob/main/showcase_bot.py">Showcase Bot</a>.</em></strong>

## Overview

This example shows:
- Language selection using built-in locales
- Custom locale management
- Dynamic content translation
- Persistent language preferences
- Using the languages() method for locale selection

## Code Example

```python
from pyrogram import Client, filters
from pykeyboard import InlineKeyboard, InlineButton
from typing import Dict, Optional
import json

app = Client("multilingual_bot")

# Language storage (in production, use a database)
user_languages: Dict[int, str] = {}

# Translation dictionaries
TRANSLATIONS = {
    "en_US": {
        "welcome": "🏠 **Welcome!**\n\nChoose your language:",
        "main_menu": "🏠 **Main Menu**\n\nWhat would you like to do?",
        "settings": "⚙️ **Settings**\n\nConfigure your preferences:",
        "language": "🌐 **Language**\n\nSelect your preferred language:",
        "profile": "👤 **Profile**\n\nManage your account:",
        "help": "ℹ️ **Help**\n\nAvailable commands:\n/start - Start the bot\n/settings - Open settings\n/help - Show this help",
        "dashboard": "📊 **Dashboard**\n\nWelcome back! Here's your overview:",
        "change_language": "🌐 Change Language",
        "back": "⬅️ Back",
        "current_lang": "Current: {lang}"
    },
    "es_ES": {
        "welcome": "🏠 **¡Bienvenido!**\n\nElige tu idioma:",
        "main_menu": "🏠 **Menú Principal**\n\n¿Qué te gustaría hacer?",
        "settings": "⚙️ **Configuración**\n\nConfigura tus preferencias:",
        "language": "🌐 **Idioma**\n\nSelecciona tu idioma preferido:",
        "profile": "👤 **Perfil**\n\nGestiona tu cuenta:",
        "help": "ℹ️ **Ayuda**\n\nComandos disponibles:\n/start - Iniciar el bot\n/settings - Abrir configuración\n/help - Mostrar esta ayuda",
        "dashboard": "📊 **Panel**\n\n¡Bienvenido de vuelta! Aquí está tu resumen:",
        "change_language": "🌐 Cambiar Idioma",
        "back": "⬅️ Atrás",
        "current_lang": "Actual: {lang}"
    },
    "fr_FR": {
        "welcome": "🏠 **Bienvenue !**\n\nChoisissez votre langue :",
        "main_menu": "🏠 **Menu Principal**\n\nQue souhaitez-vous faire ?",
        "settings": "⚙️ **Paramètres**\n\nConfigurez vos préférences :",
        "language": "🌐 **Langue**\n\nSélectionnez votre langue préférée :",
        "profile": "👤 **Profil**\n\nGérez votre compte :",
        "help": "ℹ️ **Aide**\n\nCommandes disponibles :\n/start - Démarrer le bot\n/settings - Ouvrir les paramètres\n/help - Afficher cette aide",
        "dashboard": "📊 **Tableau de Bord**\n\nBienvenue ! Voici votre aperçu :",
        "change_language": "🌐 Changer de Langue",
        "back": "⬅️ Retour",
        "current_lang": "Actuel : {lang}"
    },
    "de_DE": {
        "welcome": "🏠 **Willkommen!**\n\nWählen Sie Ihre Sprache:",
        "main_menu": "🏠 **Hauptmenü**\n\nWas möchten Sie tun?",
        "settings": "⚙️ **Einstellungen**\n\nKonfigurieren Sie Ihre Einstellungen:",
        "language": "🌐 **Sprache**\n\nWählen Sie Ihre bevorzugte Sprache:",
        "profile": "👤 **Profil**\n\nVerwalten Sie Ihr Konto:",
        "help": "ℹ️ **Hilfe**\n\nVerfügbare Befehle:\n/start - Bot starten\n/settings - Einstellungen öffnen\n/help - Diese Hilfe anzeigen",
        "dashboard": "📊 **Dashboard**\n\nWillkommen zurück! Hier ist Ihre Übersicht:",
        "change_language": "🌐 Sprache Ändern",
        "back": "⬅️ Zurück",
        "current_lang": "Aktuell: {lang}"
    }
}

def get_user_language(user_id: int) -> str:
    """Get user's preferred language, default to English."""
    return user_languages.get(user_id, "en_US")

def t(user_id: int, key: str, **kwargs) -> str:
    """Translate a key for the user's language."""
    lang = get_user_language(user_id)
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en_US"])
    text = translations.get(key, f"[{key}]")
    return text.format(**kwargs)

def create_welcome_keyboard():
    """Create language selection keyboard."""
    keyboard = InlineKeyboard()
    keyboard.languages("set_lang:{locale}", ["en_US", "es_ES", "fr_FR", "de_DE"])
    return keyboard

def create_main_menu_keyboard(user_id: int):
    """Create main menu keyboard in user's language."""
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("📊 " + t(user_id, "dashboard").split("**")[1].split("**")[0],
                    callback_data="menu:dashboard"),
        InlineButton("⚙️ " + t(user_id, "settings").split("**")[1].split("**")[0],
                    callback_data="menu:settings"),
        InlineButton("👤 " + t(user_id, "profile").split("**")[1].split("**")[0],
                    callback_data="menu:profile"),
        InlineButton("ℹ️ " + t(user_id, "help").split("**")[1].split("**")[0],
                    callback_data="menu:help")
    )
    return keyboard

def create_settings_keyboard(user_id: int):
    """Create settings keyboard in user's language."""
    keyboard = InlineKeyboard()
    current_lang = get_user_language(user_id)
    lang_name = TRANSLATIONS[current_lang]["current_lang"].format(lang=current_lang[:2].upper())

    keyboard.add(
        InlineButton(f"🌐 {t(user_id, 'change_language')} ({lang_name})",
                    callback_data="settings:language"),
        InlineButton("⬅️ " + t(user_id, "back"), callback_data="menu:main")
    )
    return keyboard

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id

    # If user hasn't selected language yet, show language selection
    if user_id not in user_languages:
        keyboard = create_welcome_keyboard()
        await message.reply_text(
            t(user_id, "welcome"),
            reply_markup=keyboard
        )
    else:
        # Show main menu in user's language
        keyboard = create_main_menu_keyboard(user_id)
        await message.reply_text(
            t(user_id, "main_menu"),
            reply_markup=keyboard
        )

@app.on_callback_query(filters.regex(r"^set_lang:"))
async def handle_language_selection(client, callback_query):
    user_id = callback_query.from_user.id
    locale = callback_query.data.split(":")[1]

    # Save user's language preference
    user_languages[user_id] = locale

    # Show main menu in selected language
    keyboard = create_main_menu_keyboard(user_id)
    await callback_query.edit_message_text(
        t(user_id, "main_menu"),
        reply_markup=keyboard
    )
    await callback_query.answer(f"Language set to {locale[:2].upper()}!")

@app.on_callback_query(filters.regex(r"^menu:"))
async def handle_menu_navigation(client, callback_query):
    user_id = callback_query.from_user.id
    menu_action = callback_query.data.split(":")[1]

    if menu_action == "main":
        keyboard = create_main_menu_keyboard(user_id)
        await callback_query.edit_message_text(
            t(user_id, "main_menu"),
            reply_markup=keyboard
        )

    elif menu_action == "settings":
        keyboard = create_settings_keyboard(user_id)
        await callback_query.edit_message_text(
            t(user_id, "settings"),
            reply_markup=keyboard
        )

    elif menu_action == "profile":
        keyboard = InlineKeyboard()
        keyboard.add(InlineButton("⬅️ " + t(user_id, "back"), callback_data="menu:main"))
        await callback_query.edit_message_text(
            t(user_id, "profile"),
            reply_markup=keyboard
        )

    elif menu_action == "help":
        keyboard = create_main_menu_keyboard(user_id)
        await callback_query.edit_message_text(
            t(user_id, "help"),
            reply_markup=keyboard
        )

    elif menu_action == "dashboard":
        keyboard = create_main_menu_keyboard(user_id)
        await callback_query.edit_message_text(
            t(user_id, "dashboard"),
            reply_markup=keyboard
        )

    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^settings:"))
async def handle_settings(client, callback_query):
    user_id = callback_query.from_user.id
    setting = callback_query.data.split(":")[1]

    if setting == "language":
        keyboard = InlineKeyboard()
        keyboard.languages("set_lang:{locale}", ["en_US", "es_ES", "fr_FR", "de_DE"])
        await callback_query.edit_message_text(
            t(user_id, "language"),
            reply_markup=keyboard
        )

    await callback_query.answer()

@app.on_message(filters.command("lang"))
async def change_language_command(client, message):
    """Allow users to change language via command."""
    user_id = message.from_user.id
    keyboard = create_welcome_keyboard()
    await message.reply_text(
        t(user_id, "welcome"),
        reply_markup=keyboard
    )

# Add custom locale example
def add_custom_locale_example():
    """Example of adding a custom locale."""
    keyboard = InlineKeyboard()

    # Add a custom locale
    keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")

    # Use it in language selection
    keyboard.languages("set_lang:{locale}", ["en_US", "en_PIRATE"])

    return keyboard

if __name__ == "__main__":
    app.run()
```

## Features Demonstrated

- Built-in locale support with 50+ languages
- Custom locale addition
- Persistent language preferences
- Dynamic content translation
- Language selection keyboards
- Translation helper functions

## Supported Languages

The example includes translations for:
- English (en_US)
- Spanish (es_ES)
- French (fr_FR)
- German (de_DE)

PyKeyboard supports 50+ built-in locales with native names and flag emojis.

## Adding Custom Languages

```python
keyboard = InlineKeyboard()
keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
```

## Running the Example

1. Install PyKeyboard: `pip install pykeyboard-kurigram`
2. Set up your bot token
3. Run the script: `python multilingual_bot.py`
4. Send `/start` to select your language
5. Navigate through the multilingual interface
6. Use `/lang` to change language anytime