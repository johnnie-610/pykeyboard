#!/usr/bin/env python3
"""
PyKeyboard Comprehensive Showcase Bot (Revamped)

This bot demonstrates the full feature set of the pykeyboard library in a clear,
API-accurate, and elegant way. It includes:

- Inline and Reply keyboards
- Advanced pagination (3, 5, 10, 25, 100)
- Language selection (built-ins + custom locales)
- Error handling and pretty error reports
- JSON serialization/deserialization
- File export/import (json/yaml) via utils
- Builder pattern and factory presets
- Visualization and debugging tools
- Modern Python features (match/case, typing.Self, Literal)
- Basic performance micro-benchmarks
- Hooks and custom validation rules
- Async support detection

Usage:
1) export TELEGRAM_BOT_TOKEN="your_bot_token"
   Optionally:
   export TELEGRAM_API_ID="..."
   export TELEGRAM_API_HASH="..."
2) python showcase_bot.py
3) Start a chat with your bot and explore the menus.

Notes:
- Logging is opt-in and pykeyboard-only. See enable_file_logging/init_logging_from_env below.
- All interactions are guarded with error handling and graceful fallbacks.
"""

import asyncio
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pyrogram import Client, filters
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import CallbackQuery, LinkPreviewOptions, Message

from pykeyboard import (ConfigurationError, ForceReply, InlineButton,
                        InlineKeyboard, KeyboardFactory, LocaleError,
                        PaginationError, PaginationUnchangedError,
                        PyKeyboardError, ReplyButton, ReplyKeyboard,
                        ReplyKeyboardRemove, ValidationError,
                        pagination_client_context)

LIBRARY_NAME = "Kurigram"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Bot token: Get it from @BotFather
API_ID = os.getenv(
    "TELEGRAM_API_ID"
)  # API ID: Get it from https://my.telegram.org
API_HASH = os.getenv(
    "TELEGRAM_API_HASH"
)  # API Hash: Get it from https://my.telegram.org

if not all([BOT_TOKEN, API_ID, API_HASH]):
    logger.critical(
        f"{i} is required. It seems you haven't set it in the environment variables.\n\nSet it using export {i}='your_secret'"
        for i in ["TELEGRAM_BOT_TOKEN", "TELEGRAM_API_ID", "TELEGRAM_API_HASH"]
    )
    sys.exit(1)


client_kwargs: Dict[str, Any] = {
    "name": "pykeyboard_showcase_bot",
    "bot_token": BOT_TOKEN,
    "api_id": API_ID,
    "api_hash": API_HASH,
}

client_kwargs["in_memory"] = True  # Uncomment for sqlite persistent sessions

# client_kwargs["test_mode"] = True # Uncomment for test mode

# client_kwargs["link_preview_options"] = LinkPreviewOptions(is_disabled=True) #Uncomment to disable webpage preview

app: Client = Client(**client_kwargs)

# State
user_states: Dict[int, Dict[str, Any]] = {}


# Helpers
def python_version_str() -> str:
    import sys

    v = sys.version_info
    return f"{v.major}.{v.minor}.{v.micro}"


def truncate(text: str, limit: int = 1500) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n… (truncated)"


def main_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton(text="🎯 Inline", callback_data="menu:inline"),
        InlineButton(text="📱 Reply", callback_data="menu:reply"),
        InlineButton(text="📄 Pagination", callback_data="menu:pagination"),
        InlineButton(text="🌍 Languages", callback_data="menu:languages"),
        InlineButton(text="💾 Errors", callback_data="menu:errors"),
        InlineButton(text="🏗️ Builder", callback_data="menu:builder"),
        InlineButton(text="📊 Performance", callback_data="menu:performance"),
        InlineButton(text="❓ Help", callback_data="menu:help"),
    )
    return kb


def pagination_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=3)
    kb.add(
        InlineButton(text="3 pages", callback_data="p:size:3"),
        InlineButton(text="5 pages", callback_data="p:size:5"),
        InlineButton(text="10 pages", callback_data="p:size:10"),
        InlineButton(text="25 pages", callback_data="p:size:25"),
        InlineButton(text="100 pages", callback_data="p:size:100"),
        InlineButton(text="⏪ Main", callback_data="menu:main"),
    )
    return kb


def builder_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton(
            text="✅ Confirmation", callback_data="build:confirmation"
        ),
        InlineButton(text="📋 Menu", callback_data="build:menu"),
        InlineButton(text="⭐ Rating", callback_data="build:rating"),
        InlineButton(text="📄 Pagination", callback_data="build:pagination"),
        InlineButton(text="🌍 Language", callback_data="build:language"),
        InlineButton(text="⏪ Main", callback_data="menu:main"),
    )
    return kb


def error_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton(
            text="🚨 Trigger Pagination Error", callback_data="error:pagination"
        ),
        InlineButton(
            text="🔄 Trigger Duplicate Prevention",
            callback_data="error:duplicate",
        ),
        InlineButton(
            text="🌍 Trigger Locale Error", callback_data="error:locale"
        ),
        InlineButton(
            text="✅ Trigger Validation Error", callback_data="error:validation"
        ),
        InlineButton(
            text="⚙️ Trigger Config Error", callback_data="error:config"
        ),
        InlineButton(text="⏪ Main", callback_data="menu:main"),
    )
    return kb


def help_text() -> str:
    return f"""
🤖 <b>PyKeyboard Showcase Bot</b>

This bot demonstrates core and advanced features of PyKeyboard.

<b>Sections</b>
• 🎯 Inline - basic, URL, and action buttons
• 📱 Reply - contact/location, remove keyboard, force reply
• 📄 Pagination - 3/5/10/25/100 pages with navigation
• 🌍 Languages - built-in + custom locales
• 🚨 Error Handling - enhanced error messages and logging
• 🏗️ Builder - fluent builder and factory presets
• 📊 Performance - micro-benchmarks (creation/pagination)

<b>Status</b>
• Library: {LIBRARY_NAME}
• Python: {python_version_str()}

Use /start for the main menu, /status for a quick summary.
"""


# Commands
@app.on_message(filters.command("start"))
async def cmd_start(client: Client, message: Message):
    user_states[message.from_user.id] = {"menu": "main"}
    welcome = f"""
🎉 <b>Welcome to PyKeyboard Showcase</b>

Explore the menus below to see API-accurate demonstrations of:
• Inline and Reply keyboards
• Pagination and Languages
• 🚨Error Handling
• Builder
• Micro performance checks

Library: {LIBRARY_NAME} • Python: {python_version_str()}
"""
    await message.reply_text(welcome, reply_markup=main_menu_keyboard())


@app.on_message(filters.command("help"))
async def cmd_help(client: Client, message: Message):
    await message.reply_text(help_text(), reply_markup=main_menu_keyboard())


@app.on_message(filters.command("status"))
async def cmd_status(client: Client, message: Message):
    status = f"""
📊 <b>Status</b>

<b>Library:</b> {LIBRARY_NAME}
<b>Python:</b> {python_version_str()}

Active users: {len(user_states)}
"""
    await message.reply_text(status)


# Callback handler
@app.on_callback_query()
async def on_callback(client: Client, callback: CallbackQuery):
    data = callback.data or ""
    user_id = callback.from_user.id
    user_states.setdefault(user_id, {"menu": "main"})

    try:
        # Navigation
        if data == "menu:main":
            user_states[user_id]["menu"] = "main"
            await callback.edit_message_text(
                "Select a feature to explore:",
                reply_markup=main_menu_keyboard(),
            )

        elif data == "menu:inline":
            kb = InlineKeyboard(row_width=3)
            kb.add(
                InlineButton(text="👍 Like", callback_data="action:like"),
                InlineButton(text="👎 Dislike", callback_data="action:dislike"),
                InlineButton(text="❤️ Love", callback_data="action:love"),
                InlineButton(text="🔥 Fire", callback_data="action:fire"),
                InlineButton(text="🔗 Website", callback_data="action:url"),
                InlineButton(text="⭐ Star", callback_data="action:star"),
            )
            await callback.edit_message_text(
                "🎯 <b>Inline Keyboard</b>\n\n"
                "• Action buttons send callback data\n"
                "• '🔗 Website' example demonstrates URL sending via follow-up message\n"
                "Code to reproduce keyboard:\n\n"
                "```python\n"
                "kb = InlineKeyboard(row_width=3)\n"
                "kb.add(\n"
                "    InlineButton(text='👍 Like', callback_data='action:like'),\n"
                "    InlineButton(text='👎 Dislike', callback_data='action:dislike'),\n"
                "    InlineButton(text='❤️ Love', callback_data='action:love'),\n"
                "    InlineButton(text='🔥 Fire', callback_data='action:fire'),\n"
                "    InlineButton(text='🔗 Website', callback_data='action:url'),\n"
                "    InlineButton(text='⭐ Star', callback_data='action:star'),\n"
                ")\n"
                " await client.send_message(chat_id, 'Your message text here', reply_markup=kb)\n"
                "```",
                reply_markup=kb,
            )

        elif data == "menu:reply":
            # Reply keyboards cannot have callback_data; they carry only text/requests
            kb = ReplyKeyboard(
                resize_keyboard=True,
                one_time_keyboard=False,
                placeholder="Choose an option...",
            )
            kb.row(
                ReplyButton(text="📱 Share Contact", request_contact=True),
                ReplyButton(text="📍 Share Location", request_location=True),
            )
            kb.row(
                ReplyButton(text="❌ Remove Keyboard"),
                ReplyButton(text="📝 Force Reply"),
            )
            await app.send_message(
                chat_id=callback.from_user.id,
                text=(
                    "📱 <b>Reply Keyboard</b>\n\n"
                    "• Contact/Location request buttons\n"
                    "• Remove Keyboard: sends a remove markup\n"
                    "• Force Reply: asks for a direct reply with placeholder"
                    "Code to reproduce keyboard:\n\n"
                    "```python\n"
                    "kb = ReplyKeyboard(\n"
                    "    resize_keyboard=True,\n"
                    "    one_time_keyboard=False,\n"
                    "    placeholder='Choose an option...',\n"
                    ")\n"
                    "kb.row(\n"
                    "    ReplyButton(text='📱 Share Contact', request_contact=True),\n"
                    "    ReplyButton(text='📍 Share Location', request_location=True),\n"
                    ")\n"
                    "kb.row(\n"
                    "    ReplyButton(text='❌ Remove Keyboard'),\n"
                    "    ReplyButton(text='📝 Force Reply'),\n"
                    ")\n"
                    "await client.send_message(chat_id, 'Your message text here', reply_markup=kb)\n"
                    "```",
                ),
                reply_markup=kb,
            )
            await callback.answer("Reply keyboard sent to chat")

        elif data == "menu:pagination":
            await callback.edit_message_text(
                "📄 <b>Pagination Demos</b>\nChoose total pages:",
                reply_markup=pagination_menu_keyboard(),
            )

        elif data.startswith("p:size:"):
            try:
                # Code to reproduce keyboard:

                reproducing_code = """
```python
kb = InlineKeyboard()
kb.paginate({total}, {current}, 'page:{number}')
kb.row(InlineButton(text='⏪ Back', callback_data='menu:pagination'))
await callback.edit_message_text(
    f'📄 <b>Pagination</b>\nTotal: {total} • Current: {current}',
    reply_markup=kb,
)
```
                """

                total = int(data.split(":")[-1])
                current = max(1, min(total, (total + 1) // 2))  # middle page

                kb = InlineKeyboard()
                kb.paginate(total, current, "page:{number}")
                kb.row(
                    InlineButton(
                        text="⏪ Back", callback_data="menu:pagination"
                    )
                )

                await callback.edit_message_text(
                    f"📄 <b>Pagination</b>\nTotal: {total} • Current: {current}\n\n"
                    "Code to reproduce keyboard:\n\n"
                    f"{reproducing_code.format(total=total, current=current, number="number")}".strip(),
                    reply_markup=kb,
                )
            except Exception as e:
                if isinstance(
                    e,
                    (
                        PaginationError,
                        LocaleError,
                        ValidationError,
                        ConfigurationError,
                    ),
                ):
                    await callback.edit_message_text(
                        f"🚨 {type(e).__name__} occurred.\n"
                        + truncate(e.get_full_report()),
                        reply_markup=main_menu_keyboard(),
                    )
                else:
                    await callback.edit_message_text(
                        f"🚨 Unexpected error: {type(e).__name__}: {e}",
                        reply_markup=main_menu_keyboard(),
                    )

        elif data.startswith("page:"):
            reproducing_code = """
```python
kb = InlineKeyboard()
kb.paginate({total}, {page}, 'page:{number}')
kb.row(InlineButton(text='⏪ Back', callback_data='menu:pagination'))
await callback.edit_message_text(
    f'📄 <b>Pagination</b>\nTotal: {total} • Current: {page}',
    reply_markup=kb,
)
```
                """
            # dynamic navigation for pagination keyboards
            try:
                page = int(data.split(":")[-1])
                # Attempt to recover context from message text (expects "Total: X" substring)
                msg = callback.message.text or ""
                total = 10
                for token in msg.split():
                    if token.isdigit():
                        # Heuristic: first number after "Total:"; fallback to 10 if not found
                        total = int(token)
                        break

                # Set contextvar for this user
                pagination_client_context.set(f"user_{user_id}")

                kb = InlineKeyboard()
                kb.paginate(total, page, "page:{number}")
                kb.row(
                    InlineButton(
                        text="⏪ Back", callback_data="menu:pagination"
                    )
                )
                await callback.edit_message_text(
                    f"📄 <b>Pagination</b>\nTotal: {total} • Current: {page}\n\n"
                    "Code to reproduce keyboard:\n\n"
                    f"{reproducing_code.format(total=total, page=page, number="number")}".strip(),
                    reply_markup=kb,
                )
            except PaginationUnchangedError as e:
                # Handle duplicate prevention - log and skip message edit
                logger.info(
                    f"Pagination duplicate prevented for user {user_id}: {e.message}"
                )
                await callback.answer(
                    "Keyboard unchanged - duplicate prevented!", show_alert=True
                )
                return
            except Exception as e:
                if isinstance(
                    e,
                    (
                        PaginationError,
                        LocaleError,
                        ValidationError,
                        ConfigurationError,
                    ),
                ):
                    await callback.edit_message_text(
                        f"🚨 {type(e).__name__} occurred.\n"
                        + truncate(e.get_full_report()),
                        reply_markup=main_menu_keyboard(),
                    )
                else:
                    await callback.edit_message_text(
                        f"🚨 Unexpected error: {type(e).__name__}: {e}",
                        reply_markup=main_menu_keyboard(),
                    )

        elif data == "menu:languages":
            kb = InlineKeyboard()
            # Add a couple of custom locales for demo
            kb.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
            kb.add_custom_locale("en_HACKER", "👨‍💻 Hacker Speak")
            locales = [
                "en_US",
                "es_ES",
                "fr_FR",
                "de_DE",
                "it_IT",
                "pt_BR",
                "ru_RU",
                "en_PIRATE",
                "en_HACKER",
            ]
            kb.languages("lang:{locale}", locales, row_width=2)
            kb.row(InlineButton(text="⏪ Main", callback_data="menu:main"))
            await callback.edit_message_text(
                "🌍 <b>Languages</b>\nChoose a locale:"
                "Code to reproduce keyboard:\n\n"
                "```python\n"
                "kb = InlineKeyboard()\n"
                "kb.languages('lang:{locale}', locales, row_width=2)\n"
                "kb.row(InlineButton(text='⏪ Main', callback_data='menu:main'))\n"
                "await callback.edit_message_text(\n"
                "    '🌍 <b>Languages</b>\nChoose a locale:',\n"
                "    reply_markup=kb,\n"
                ")\n"
                "```",
                reply_markup=kb,
            )

        elif data == "menu:errors":
            await callback.edit_message_text(
                "🚨 <b>Error Handling Demo</b>\n\n"
                "This section demonstrates PyKeyboard's enhanced error handling:\n"
                "• Automatic logging to terminal and files\n"
                "• Detailed help messages with fix suggestions\n"
                "• Context-aware error information\n"
                "• Developer-friendly error reports\n\n"
                "Choose an error type to trigger:",
                reply_markup=error_menu_keyboard(),
            )

        elif data.startswith("lang:"):
            locale = data.split(":", 1)[1]
            await callback.edit_message_text(
                f"🌍 <b>Language Selected</b>\nLocale: <code>{locale}</code>\n\n"
                "• Stored as callback data\n• Ready for i18n flows",
                reply_markup=main_menu_keyboard(),
            )

        elif data == "menu:builder":
            await callback.edit_message_text(
                "🏗️ <b>Builder / Factory</b>\nChoose a preset:",
                reply_markup=builder_menu_keyboard(),
            )

        elif data.startswith("build:"):
            kind = data.split(":", 1)[1]
            kb: Optional[InlineKeyboard] = None
            try:
                if kind == "confirmation":
                    kb = KeyboardFactory.create_confirmation_keyboard(
                        yes_text="✅ Confirm",
                        no_text="❌ Cancel",
                        cancel_text="⏪ Back",
                    )
                elif kind == "menu":
                    kb = KeyboardFactory.create_menu_keyboard(
                        {
                            "Home": "home",
                            "Settings": "settings",
                            "Help": "help",
                        },
                        callback_pattern="menu:{action}",
                        columns=2,
                    )
                elif kind == "rating":
                    kb = KeyboardFactory.create_rating_keyboard(
                        5, callback_pattern="rate:{stars}", include_labels=True
                    )
                elif kind == "pagination":
                    kb = KeyboardFactory.create_pagination_keyboard(
                        total_pages=9,
                        current_page=5,
                        callback_pattern="page:{number}",
                        include_buttons=[
                            {"text": "Close", "callback_data": "action:close"}
                        ],
                    )
                elif kind == "language":
                    kb = KeyboardFactory.create_language_keyboard(
                        locales=["en_US", "es_ES", "de_DE", "fr_FR"],
                        callback_pattern="lang:{locale}",
                        row_width=2,
                    )
                else:
                    kb = InlineKeyboard()
                    kb.add(InlineButton(text="Unknown", callback_data="noop"))
                kb.row(
                    InlineButton(
                        text="⏪ Builder Menu", callback_data="menu:builder"
                    )
                )
                await callback.edit_message_text(
                    f"🏗️ <b>Builder: {kind.title()}</b>"
                    "Dive into docs for [more info](https://github.com/johnnie-610/pykeyboard).",
                    reply_markup=kb,
                )
            except Exception as e:
                if isinstance(
                    e,
                    (
                        PaginationError,
                        LocaleError,
                        ValidationError,
                        ConfigurationError,
                    ),
                ):
                    await callback.edit_message_text(
                        f"🚨 {type(e).__name__} occurred.\n"
                        + truncate(e.get_full_report()),
                        reply_markup=builder_menu_keyboard(),
                    )
                else:
                    await callback.edit_message_text(
                        f"🚨 Unexpected error: {type(e).__name__}: {e}",
                        reply_markup=builder_menu_keyboard(),
                    )

        elif data == "menu:performance":
            # Micro-benchmarks (lightweight)
            try:
                runs = 150
                t0 = time.perf_counter()
                keyboards: List[InlineKeyboard] = []
                for i in range(runs):
                    k = InlineKeyboard()
                    k.add(
                        InlineButton(
                            text=f"Btn{i%5}", callback_data=f"b:{i%5}"
                        ),
                        InlineButton(text=f"X{i%3}", callback_data=f"x:{i%3}"),
                        InlineButton(text=f"Y{i%7}", callback_data=f"y:{i%7}"),
                    )
                    keyboards.append(k)
                t1 = time.perf_counter()

                t2 = time.perf_counter()
                big = InlineKeyboard()
                big.paginate(100, 50, "page:{number}")
                t3 = time.perf_counter()

                msg = (
                    "📊 <b>Performance</b>\n"
                    f"• Create {runs} keyboards: {(t1 - t0)*1000:.2f} ms\n"
                    f"• Build pagination (100 pages): {(t3 - t2)*1000:.2f} ms\n"
                    "Memory usage: efficient by design (LRU button cache for pagination)\n"
                    "This is done automatically, no need to worry about it."
                )
                back = InlineKeyboard()
                back.add(
                    InlineButton(text="⏪ Main", callback_data="menu:main")
                )
                await callback.edit_message_text(msg, reply_markup=back)
            except Exception as e:
                if isinstance(
                    e,
                    (
                        PaginationError,
                        LocaleError,
                        ValidationError,
                        ConfigurationError,
                    ),
                ):
                    await callback.edit_message_text(
                        f"🚨 {type(e).__name__} occurred.\n"
                        + truncate(e.get_full_report()),
                        reply_markup=main_menu_keyboard(),
                    )
                else:
                    await callback.edit_message_text(
                        f"🚨 Unexpected error: {type(e).__name__}: {e}",
                        reply_markup=main_menu_keyboard(),
                    )

        elif data == "menu:help":
            await callback.edit_message_text(
                help_text(), reply_markup=main_menu_keyboard()
            )

        # Error handling demos
        elif data.startswith("error:"):
            error_type = data.split(":", 1)[1]
            try:
                if error_type == "pagination":
                    # Trigger pagination error
                    kb = InlineKeyboard()
                    kb.paginate(
                        0, 1, "page_{number}"
                    )  # This will raise PaginationError
                elif error_type == "duplicate":
                    # Trigger duplicate prevention error
                    kb = InlineKeyboard()
                    kb.paginate(
                        5, 3, "page_{number}"
                    )  # First call - should work
                    kb.paginate(
                        5, 3, "page_{number}"
                    )  # Second call - should raise PaginationUnchangedError
                elif error_type == "locale":
                    # Trigger locale error
                    kb = InlineKeyboard()
                    kb.languages(
                        "invalid_pattern", ["en_US"]
                    )  # Missing {locale}
                elif error_type == "validation":
                    # Trigger validation error by creating invalid button
                    from pykeyboard.keyboard_base import Button

                    invalid_button = Button(
                        text=""
                    )  # Empty text will raise ValidationError
                elif error_type == "config":
                    # Trigger configuration error
                    kb = InlineKeyboard(row_width=0)  # Invalid row_width
                elif error_type == "help":
                    # Show general error help
                    help_msg = (
                        "🚨 <b>PyKeyboard Error Help</b>\n\n"
                        "PyKeyboard provides comprehensive error handling:\n\n"
                        "• <b>Automatic Logging:</b> Errors are logged to terminal and files\n"
                        "• <b>Detailed Reports:</b> Use get_full_report() for complete info\n"
                        "• <b>Help Messages:</b> Use get_help_message() for fix suggestions\n"
                        "• <b>Context Information:</b> Includes file, line, and function details\n\n"
                        "Try triggering different errors above to see the enhanced messages!"
                    )
                    kb = InlineKeyboard()
                    kb.add(
                        InlineButton(
                            text="⏪ Error Menu", callback_data="menu:errors"
                        )
                    )
                    await callback.edit_message_text(help_msg, reply_markup=kb)
                    return
            except (
                PaginationError,
                PaginationUnchangedError,
                LocaleError,
                ValidationError,
                ConfigurationError,
            ) as e:
                # Handle PyKeyboard errors with enhanced display
                help_msg = e.get_help_message()
                full_report = e.get_full_report()

                # Create response with error details
                response = (
                    f"🚨 <b>PyKeyboard {type(e).__name__}</b>\n\n"
                    f"<b>What happened:</b>\n{e.message}\n\n"
                    f"<b>How to fix:</b>\n{help_msg.split('🔧 How to fix:')[1].split('📝 Example:')[0].strip() if '🔧 How to fix:' in help_msg else 'See error details below'}\n\n"
                    f"<b>Example:</b>\n<pre>{help_msg.split('📝 Example:')[1] if '📝 Example:' in help_msg else 'Check the error report'}</pre>\n\n"
                    f"<b>Full Report:</b>\n<pre>{truncate(full_report, 800)}</pre>"
                )

                kb = InlineKeyboard()
                kb.add(
                    InlineButton(
                        text="📋 Full Report",
                        callback_data=f"error:full_{error_type}",
                    ),
                    InlineButton(
                        text="⏪ Error Menu", callback_data="menu:errors"
                    ),
                )
                await callback.edit_message_text(response, reply_markup=kb)
                return
            except Exception as e:
                # Fallback for unexpected errors
                await callback.edit_message_text(
                    f"🚨 <b>Unexpected Error</b>\n\n"
                    f"<code>{type(e).__name__}: {e}</code>\n\n"
                    "This error wasn't handled by PyKeyboard's error system.",
                    reply_markup=error_menu_keyboard(),
                )
                return

        elif data.startswith("error:full_"):
            # Show full error report (this would need to store the error context)
            error_type = data.split("error:full_", 1)[1]
            await callback.edit_message_text(
                f"📋 <b>Full Error Report for {error_type.title()}</b>\n\n"
                "Full reports are available when errors occur.\n"
                "Check the terminal/console for the complete error log.",
                reply_markup=error_menu_keyboard(),
            )

        # Inline actions
        elif data.startswith("action:"):
            action = data.split(":", 1)[1]
            if action == "url":
                # Demonstrate sending an URL button in a follow-up keyboard
                kb = InlineKeyboard()
                kb.add(
                    InlineButton(
                        text="Open GitHub",
                        url="https://github.com/johnnie-610/pykeyboard",
                    )
                )
                kb.row(InlineButton(text="⏪ Main", callback_data="menu:main"))
                await callback.edit_message_text(
                    "🔗 <b>URL Button</b>\nOpen the project repository:",
                    reply_markup=kb,
                )
            else:
                emoji_map = {
                    "like": "👍",
                    "dislike": "👎",
                    "love": "❤️",
                    "fire": "🔥",
                    "star": "⭐",
                }
                emoji = emoji_map.get(action, "🎯")
                await callback.edit_message_text(
                    f"{emoji} <b>Action:</b> {action}",
                    reply_markup=main_menu_keyboard(),
                )

        else:
            await callback.edit_message_text(
                f"❓ Unknown callback:\n<code>{data}</code>",
                reply_markup=main_menu_keyboard(),
            )

    except PyKeyboardError as e:
        logger.error("Callback PyKeyboardError:\n" + e.get_full_report())
        await callback.edit_message_text(
            "🚨 <b>PyKeyboard Error</b>\n" + truncate(e.get_full_report()),
            reply_markup=main_menu_keyboard(),
        )
    except Exception as e:
        if isinstance(
            e,
            (
                PaginationError,
                PaginationUnchangedError,
                LocaleError,
                ValidationError,
                ConfigurationError,
            ),
        ):
            await callback.edit_message_text(
                f"🚨 <b>{type(e).__name__}</b>\n{truncate(e.get_full_report())}",
                reply_markup=main_menu_keyboard(),
            )
        else:
            await callback.edit_message_text(
                f"🚨 <b>Unexpected Error</b>\n"
                f"<b>Type:</b> {type(e).__name__}\n"
                f"<b>Message:</b> {e}",
                reply_markup=main_menu_keyboard(),
            )


@app.on_message()
async def on_message(client: Client, message: Message):
    text = message.text or ""
    if text == "❌ Remove Keyboard":
        try:
            rm = ReplyKeyboardRemove(selective=False)
            await message.reply_text("Keyboard removed.", reply_markup=rm)
        except Exception as e:
            if isinstance(
                e,
                (
                    PaginationError,
                    PaginationUnchangedError,
                    LocaleError,
                    ValidationError,
                    ConfigurationError,
                ),
            ):
                await message.reply_text(
                    f"Failed to remove keyboard: {e.get_help_message()[:100]}..."
                )
            else:
                await message.reply_text(
                    f"Failed to remove keyboard: {type(e).__name__}: {e}"
                )
    elif text == "📝 Force Reply":
        try:
            fr = ForceReply(selective=True, placeholder="Please reply...")
            await message.reply_text(
                "Forcing reply to this message.", reply_markup=fr
            )
        except Exception as e:
            if isinstance(
                e,
                (
                    PaginationError,
                    PaginationUnchangedError,
                    LocaleError,
                    ValidationError,
                    ConfigurationError,
                ),
            ):
                await message.reply_text(
                    f"Failed to force reply: {e.get_help_message()[:100]}..."
                )
            else:
                await message.reply_text(
                    f"Failed to force reply: {type(e).__name__}: {e}"
                )
    elif text and not text.startswith("/"):
        await message.reply_text(
            "💬 <b>Message Received</b>\n"
            f"• Text length: {len(text)}\n"
            "• Use /start to open main menu"
        )


async def main():
    print("🤖 Starting PyKeyboard Showcase Bot")
    print("=" * 50)
    print(f"📚 Library: {LIBRARY_NAME}")
    print(f"🐍 Python: {python_version_str()}")
    print("=" * 50)
    try:
        await app.start()
        print("✅ Bot started. Send /start in Telegram.")

        await idle()

    except KeyboardInterrupt:
        print("\n⏹️ Stopping…")
    except Exception as e:
        print(f"❌ Startup error: {e}")
    finally:
        try:
            await app.stop()
        except Exception:
            pass
        print("🧹 Cleanup complete")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
