#!/usr/bin/env python3
"""
PyKeyboard Showcase Bot

Demonstrates the full feature set of the pykeyboard library:

- Inline and Reply keyboards
- Pagination with navigation (3, 5, 10, 25, 100 pages)
- Language selection (built-in + custom locales)
- Error handling with structured error classes
- Builder pattern and factory presets
- Button validation hooks
- Performance micro-benchmarks

Each demo includes a reproducible code snippet.

Usage:
    export TELEGRAM_BOT_TOKEN="..."
    export TELEGRAM_API_ID="..."
    export TELEGRAM_API_HASH="..."
    python showcase_bot.py
"""

import asyncio
import logging
import os
import sys
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pyrogram import Client, filters
from pyrogram.methods.utilities.idle import idle
from pyrogram.types import CallbackQuery, Message

from pykeyboard import (
    ButtonValidator,
    ConfigurationError,
    ForceReply,
    InlineButton,
    InlineKeyboard,
    KeyboardBuilder,
    KeyboardFactory,
    LocaleError,
    PaginationError,
    PaginationUnchangedError,
    PyKeyboardError,
    ReplyButton,
    ReplyKeyboard,
    ReplyKeyboardRemove,
    ValidationError,
    pagination_client_context,
    validate_button,
)

# ─── Configuration ────────────────────────────────────────────────────────────

LIBRARY_NAME = "Kurigram"
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

REQUIRED_VARS = {"TELEGRAM_BOT_TOKEN": BOT_TOKEN, "TELEGRAM_API_ID": API_ID, "TELEGRAM_API_HASH": API_HASH}
missing = [k for k, v in REQUIRED_VARS.items() if not v]
if missing:
    for var in missing:
        logger.critical(f"{var} is required. Set it with: export {var}='your_value'")
    sys.exit(1)

app = Client(
    name="pykeyboard_showcase_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
)

# ─── State ────────────────────────────────────────────────────────────────────

user_states: dict[int, dict[str, object]] = {}

# ─── Helpers ──────────────────────────────────────────────────────────────────


def truncate(text: str, limit: int = 1500) -> str:
    """Truncate text to a maximum length, appending an ellipsis if needed."""
    return text if len(text) <= limit else text[:limit] + "\n\n… (truncated)"


def code_block(code: str) -> str:
    """Wrap code in a Telegram-friendly preformatted block."""
    return f"<pre>{code.strip()}</pre>"


# ─── Menu keyboards ──────────────────────────────────────────────────────────


def main_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton(text="🎯 Inline", callback_data="menu:inline"),
        InlineButton(text="📱 Reply", callback_data="menu:reply"),
        InlineButton(text="📄 Pagination", callback_data="menu:pagination"),
        InlineButton(text="🌍 Languages", callback_data="menu:languages"),
        InlineButton(text="🚨 Errors", callback_data="menu:errors"),
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
        InlineButton(text="✅ Confirmation", callback_data="build:confirmation"),
        InlineButton(text="📋 Menu", callback_data="build:menu"),
        InlineButton(text="⭐ Rating", callback_data="build:rating"),
        InlineButton(text="📄 Pagination", callback_data="build:pagination"),
        InlineButton(text="🌍 Language", callback_data="build:language"),
        InlineButton(text="🔧 Fluent Builder", callback_data="build:fluent"),
        InlineButton(text="🪝 Hooks & Validation", callback_data="build:hooks"),
        InlineButton(text="⏪ Main", callback_data="menu:main"),
    )
    return kb


def error_menu_keyboard() -> InlineKeyboard:
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton(text="🚨 Pagination Error", callback_data="error:pagination"),
        InlineButton(text="🔄 Duplicate Prevention", callback_data="error:duplicate"),
        InlineButton(text="🌍 Locale Error", callback_data="error:locale"),
        InlineButton(text="✅ Validation Error", callback_data="error:validation"),
        InlineButton(text="⚙️ Config Error", callback_data="error:config"),
        InlineButton(text="⏪ Main", callback_data="menu:main"),
    )
    return kb


# ─── Help text ────────────────────────────────────────────────────────────────


def help_text() -> str:
    return (
        "🤖 <b>PyKeyboard Showcase Bot</b>\n\n"
        "Demonstrates the full feature set of PyKeyboard.\n\n"
        "<b>Sections</b>\n"
        "• 🎯 Inline — action, URL, and reaction buttons\n"
        "• 📱 Reply — contact/location, remove keyboard, force reply\n"
        "• 📄 Pagination — 3/5/10/25/100 pages with navigation\n"
        "• 🌍 Languages — built-in + custom locales\n"
        "• 🚨 Errors — structured error classes with error codes\n"
        "• 🏗️ Builder — fluent builder, factory presets, validation hooks\n"
        "• 📊 Performance — micro-benchmarks\n\n"
        f"<b>Library:</b> {LIBRARY_NAME} • <b>Python:</b> {PYTHON_VERSION}\n\n"
        "Use /start for the main menu."
    )


# ─── Commands ─────────────────────────────────────────────────────────────────


@app.on_message(filters.command("start"))
async def cmd_start(_client: Client, message: Message):
    user_states[message.from_user.id] = {"menu": "main"}
    await message.reply_text(
        "🎉 <b>Welcome to PyKeyboard Showcase</b>\n\n"
        "Explore interactive demos of every PyKeyboard feature.\n"
        "Each section includes a reproducible code snippet.\n\n"
        f"<b>Library:</b> {LIBRARY_NAME} • <b>Python:</b> {PYTHON_VERSION}",
        reply_markup=main_menu_keyboard(),
    )


@app.on_message(filters.command("help"))
async def cmd_help(_client: Client, message: Message):
    await message.reply_text(help_text(), reply_markup=main_menu_keyboard())


@app.on_message(filters.command("status"))
async def cmd_status(_client: Client, message: Message):
    await message.reply_text(
        "📊 <b>Status</b>\n\n"
        f"<b>Library:</b> {LIBRARY_NAME}\n"
        f"<b>Python:</b> {PYTHON_VERSION}\n"
        f"<b>Active users:</b> {len(user_states)}",
    )


# ─── Callback router ─────────────────────────────────────────────────────────


@app.on_callback_query()
async def on_callback(_client: Client, callback: CallbackQuery):
    data = callback.data or ""
    user_id = callback.from_user.id
    user_states.setdefault(user_id, {"menu": "main"})

    try:
        match data:
            # ── Navigation ────────────────────────────────────────────────
            case "menu:main":
                user_states[user_id]["menu"] = "main"
                await callback.edit_message_text(
                    "Select a feature to explore:",
                    reply_markup=main_menu_keyboard(),
                )

            # ── Inline Keyboard ───────────────────────────────────────────
            case "menu:inline":
                await _demo_inline(callback)

            # ── Reply Keyboard ────────────────────────────────────────────
            case "menu:reply":
                await _demo_reply(callback)

            # ── Pagination ────────────────────────────────────────────────
            case "menu:pagination":
                await callback.edit_message_text(
                    "📄 <b>Pagination Demos</b>\n\nChoose total pages:",
                    reply_markup=pagination_menu_keyboard(),
                )

            # ── Languages ─────────────────────────────────────────────────
            case "menu:languages":
                await _demo_languages(callback)

            # ── Errors ────────────────────────────────────────────────────
            case "menu:errors":
                await callback.edit_message_text(
                    "🚨 <b>Error Handling Demo</b>\n\n"
                    "PyKeyboard uses structured error classes:\n"
                    "• Each has an <code>error_code</code> attribute\n"
                    "• Data-carrying fields: <code>.param</code>, <code>.value</code>, <code>.reason</code>\n"
                    "• All inherit from <code>PyKeyboardError</code>\n\n"
                    "Choose an error type to trigger:",
                    reply_markup=error_menu_keyboard(),
                )

            # ── Builder ───────────────────────────────────────────────────
            case "menu:builder":
                await callback.edit_message_text(
                    "🏗️ <b>Builder & Factory</b>\n\nChoose a preset:",
                    reply_markup=builder_menu_keyboard(),
                )

            # ── Performance ───────────────────────────────────────────────
            case "menu:performance":
                await _demo_performance(callback)

            # ── Help ──────────────────────────────────────────────────────
            case "menu:help":
                await callback.edit_message_text(
                    help_text(), reply_markup=main_menu_keyboard()
                )

            # ── Dynamic routing ───────────────────────────────────────────
            case _ if data.startswith("p:size:"):
                await _handle_pagination_init(callback, data)

            case _ if data.startswith("page:"):
                await _handle_pagination_nav(callback, data, user_id)

            case _ if data.startswith("lang:"):
                locale = data.split(":", 1)[1]
                await callback.edit_message_text(
                    f"🌍 <b>Language Selected</b>\n"
                    f"Locale: <code>{locale}</code>\n\n"
                    "• Stored as callback data\n"
                    "• Ready for i18n flows",
                    reply_markup=main_menu_keyboard(),
                )

            case _ if data.startswith("build:"):
                await _handle_builder(callback, data.split(":", 1)[1])

            case _ if data.startswith("error:"):
                await _handle_error_demo(callback, data.split(":", 1)[1])

            case _ if data.startswith("action:"):
                await _handle_action(callback, data.split(":", 1)[1])

            case _:
                await callback.edit_message_text(
                    f"❓ Unknown callback:\n<code>{data}</code>",
                    reply_markup=main_menu_keyboard(),
                )

    except PyKeyboardError as e:
        logger.error(f"PyKeyboardError in callback: {e}")
        await callback.edit_message_text(
            f"🚨 <b>PyKeyboard Error</b>\n{truncate(str(e))}",
            reply_markup=main_menu_keyboard(),
        )
    except Exception as e:
        logger.exception(f"Unexpected error in callback: {e}")
        await callback.edit_message_text(
            f"🚨 <b>Unexpected Error</b>\n"
            f"<b>Type:</b> {type(e).__name__}\n"
            f"<b>Message:</b> {e}",
            reply_markup=main_menu_keyboard(),
        )


# ─── Demo handlers ────────────────────────────────────────────────────────────


async def _demo_inline(callback: CallbackQuery) -> None:
    """Inline keyboard with action buttons."""
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
        "• '🔗 Website' demonstrates URL buttons\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            "kb = InlineKeyboard(row_width=3)\n"
            "kb.add(\n"
            "    InlineButton(text='👍 Like', callback_data='action:like'),\n"
            "    InlineButton(text='👎 Dislike', callback_data='action:dislike'),\n"
            "    InlineButton(text='❤️ Love', callback_data='action:love'),\n"
            ")\n"
            "await msg.reply('Pick a reaction:', reply_markup=kb)"
        ),
        reply_markup=kb,
    )


async def _demo_reply(callback: CallbackQuery) -> None:
    """Reply keyboard with contact/location requests."""
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
            "• Force Reply: asks for a direct reply\n\n"
            "<b>Code to reproduce:</b>\n\n"
            + code_block(
                "kb = ReplyKeyboard(\n"
                "    resize_keyboard=True,\n"
                "    placeholder='Choose an option...',\n"
                ")\n"
                "kb.row(\n"
                "    ReplyButton(text='📱 Contact', request_contact=True),\n"
                "    ReplyButton(text='📍 Location', request_location=True),\n"
                ")\n"
                "await msg.reply('Pick an option:', reply_markup=kb)"
            )
        ),
        reply_markup=kb,
    )
    await callback.answer("Reply keyboard sent to chat")


async def _demo_languages(callback: CallbackQuery) -> None:
    """Language selection with built-in and custom locales."""
    kb = InlineKeyboard()
    kb.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
    kb.add_custom_locale("en_HACKER", "👨‍💻 Hacker Speak")
    locales = [
        "en_US", "es_ES", "fr_FR", "de_DE",
        "it_IT", "pt_BR", "ru_RU",
        "en_PIRATE", "en_HACKER",
    ]
    kb.languages("lang:{locale}", locales, row_width=2)
    kb.row(InlineButton(text="⏪ Main", callback_data="menu:main"))
    await callback.edit_message_text(
        "🌍 <b>Languages</b>\n\n"
        "Choose a locale:\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            "kb = InlineKeyboard()\n"
            "kb.add_custom_locale('en_PIRATE', '🏴‍☠️ Pirate English')\n"
            "locales = ['en_US', 'es_ES', 'fr_FR', 'de_DE']\n"
            "kb.languages('lang:{locale}', locales, row_width=2)\n"
            "await msg.reply('Choose a locale:', reply_markup=kb)"
        ),
        reply_markup=kb,
    )


async def _demo_performance(callback: CallbackQuery) -> None:
    """Micro-benchmarks for keyboard creation and pagination."""
    runs = 150

    t0 = time.perf_counter()
    for i in range(runs):
        k = InlineKeyboard()
        k.add(
            InlineButton(text=f"Btn{i % 5}", callback_data=f"b:{i % 5}"),
            InlineButton(text=f"X{i % 3}", callback_data=f"x:{i % 3}"),
            InlineButton(text=f"Y{i % 7}", callback_data=f"y:{i % 7}"),
        )
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    big = InlineKeyboard()
    big.paginate(100, 50, "page:{number}")
    t3 = time.perf_counter()

    back = InlineKeyboard()
    back.add(InlineButton(text="⏪ Main", callback_data="menu:main"))
    await callback.edit_message_text(
        "📊 <b>Performance</b>\n\n"
        f"• Create {runs} keyboards: <b>{(t1 - t0) * 1000:.2f} ms</b>\n"
        f"• Build pagination (100 pages): <b>{(t3 - t2) * 1000:.2f} ms</b>\n"
        "• LRU button cache for pagination (automatic)\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            "import time\n\n"
            "t0 = time.perf_counter()\n"
            "for i in range(150):\n"
            "    k = InlineKeyboard()\n"
            "    k.add(InlineButton(text=f'Btn{i}', callback_data=f'b:{i}'))\n"
            "elapsed = (time.perf_counter() - t0) * 1000\n"
            "print(f'Created 150 keyboards in {elapsed:.2f}ms')"
        ),
        reply_markup=back,
    )


# ─── Pagination handlers ─────────────────────────────────────────────────────


async def _handle_pagination_init(callback: CallbackQuery, data: str) -> None:
    """Initialize a pagination demo with N pages."""
    total = int(data.split(":")[-1])
    current = max(1, min(total, (total + 1) // 2))

    kb = InlineKeyboard()
    kb.paginate(total, current, "page:{number}")
    kb.row(InlineButton(text="⏪ Back", callback_data="menu:pagination"))

    await callback.edit_message_text(
        f"📄 <b>Pagination</b>\n"
        f"Total: {total} • Current: {current}\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            f"kb = InlineKeyboard()\n"
            f"kb.paginate({total}, {current}, 'page:{{number}}')\n"
            f"await msg.reply('Navigate:', reply_markup=kb)"
        ),
        reply_markup=kb,
    )


async def _handle_pagination_nav(
    callback: CallbackQuery, data: str, user_id: int
) -> None:
    """Navigate to a specific page in a pagination demo."""
    try:
        page = int(data.split(":")[-1])

        # Recover total from message text (expects "Total: X" substring)
        msg_text = callback.message.text or ""
        total = 10
        for token in msg_text.split():
            if token.isdigit():
                total = int(token)
                break

        pagination_client_context.set(f"user_{user_id}")

        kb = InlineKeyboard()
        kb.paginate(total, page, "page:{number}")
        kb.row(InlineButton(text="⏪ Back", callback_data="menu:pagination"))

        await callback.edit_message_text(
            f"📄 <b>Pagination</b>\n"
            f"Total: {total} • Current: {page}\n\n"
            "<b>Code to reproduce:</b>\n\n"
            + code_block(
                f"kb = InlineKeyboard()\n"
                f"kb.paginate({total}, {page}, 'page:{{number}}')\n"
                f"await msg.reply('Navigate:', reply_markup=kb)"
            ),
            reply_markup=kb,
        )
    except PaginationUnchangedError:
        await callback.answer(
            "Keyboard unchanged — duplicate prevented!", show_alert=True
        )


# ─── Builder handlers ────────────────────────────────────────────────────────

# Mapping of factory kind → (factory call, code snippet)
_FACTORY_BUILDERS: dict[str, tuple[callable, str]] = {}


def _register_factory(kind: str, code: str):
    """Decorator to register a factory builder with its code snippet."""
    def decorator(func):
        _FACTORY_BUILDERS[kind] = (func, code)
        return func
    return decorator


@_register_factory("confirmation", (
    "kb = KeyboardFactory.create_confirmation_keyboard(\n"
    "    yes_text='✅ Confirm',\n"
    "    no_text='❌ Cancel',\n"
    "    cancel_text='⏪ Back',\n"
    ")"
))
def _build_confirmation():
    return KeyboardFactory.create_confirmation_keyboard(
        yes_text="✅ Confirm", no_text="❌ Cancel", cancel_text="⏪ Back",
    )


@_register_factory("menu", (
    "kb = KeyboardFactory.create_menu_keyboard(\n"
    "    {'Home': 'home', 'Settings': 'settings', 'Help': 'help'},\n"
    "    callback_pattern='menu:{action}',\n"
    "    columns=2,\n"
    ")"
))
def _build_menu():
    return KeyboardFactory.create_menu_keyboard(
        {"Home": "home", "Settings": "settings", "Help": "help"},
        callback_pattern="menu:{action}",
        columns=2,
    )


@_register_factory("rating", (
    "kb = KeyboardFactory.create_rating_keyboard(\n"
    "    5,\n"
    "    callback_pattern='rate:{stars}',\n"
    "    include_labels=True,\n"
    ")"
))
def _build_rating():
    return KeyboardFactory.create_rating_keyboard(
        5, callback_pattern="rate:{stars}", include_labels=True,
    )


@_register_factory("pagination", (
    "kb = KeyboardFactory.create_pagination_keyboard(\n"
    "    total_pages=9,\n"
    "    current_page=5,\n"
    "    callback_pattern='page:{number}',\n"
    "    include_buttons=[{'text': 'Close', 'callback_data': 'close'}],\n"
    ")"
))
def _build_pagination():
    return KeyboardFactory.create_pagination_keyboard(
        total_pages=9,
        current_page=5,
        callback_pattern="page:{number}",
        include_buttons=[{"text": "Close", "callback_data": "action:close"}],
    )


@_register_factory("language", (
    "kb = KeyboardFactory.create_language_keyboard(\n"
    "    locales=['en_US', 'es_ES', 'de_DE', 'fr_FR'],\n"
    "    callback_pattern='lang:{locale}',\n"
    "    row_width=2,\n"
    ")"
))
def _build_language():
    return KeyboardFactory.create_language_keyboard(
        locales=["en_US", "es_ES", "de_DE", "fr_FR"],
        callback_pattern="lang:{locale}",
        row_width=2,
    )


async def _handle_builder(callback: CallbackQuery, kind: str) -> None:
    """Route builder/factory demos."""
    match kind:
        case "fluent":
            await _demo_fluent_builder(callback)
        case "hooks":
            await _demo_hooks(callback)
        case _ if kind in _FACTORY_BUILDERS:
            builder_fn, snippet = _FACTORY_BUILDERS[kind]
            kb = builder_fn()
            kb.row(InlineButton(text="⏪ Builder Menu", callback_data="menu:builder"))
            await callback.edit_message_text(
                f"🏗️ <b>Factory: {kind.title()}</b>\n\n"
                "<b>Code to reproduce:</b>\n\n"
                + code_block(snippet),
                reply_markup=kb,
            )
        case _:
            kb = InlineKeyboard()
            kb.add(InlineButton(text="Unknown preset", callback_data="noop"))
            kb.row(InlineButton(text="⏪ Builder Menu", callback_data="menu:builder"))
            await callback.edit_message_text(
                f"❓ Unknown builder preset: <code>{kind}</code>",
                reply_markup=kb,
            )


async def _demo_fluent_builder(callback: CallbackQuery) -> None:
    """Demonstrate the fluent KeyboardBuilder API."""
    kb = (
        KeyboardBuilder(InlineKeyboard())
        .add_row("🏠 Home", "⚙️ Settings")
        .add_row("📊 Stats", "🆘 Help", "❓ FAQ")
        .add_navigation_buttons(10, 5, "page_{number}")
        .build()
    )
    kb.row(InlineButton(text="⏪ Builder Menu", callback_data="menu:builder"))
    await callback.edit_message_text(
        "🔧 <b>Fluent Builder API</b>\n\n"
        "Build keyboards with method chaining:\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            "kb = (\n"
            "    KeyboardBuilder(InlineKeyboard())\n"
            "    .add_row('🏠 Home', '⚙️ Settings')\n"
            "    .add_row('📊 Stats', '🆘 Help', '❓ FAQ')\n"
            "    .add_navigation_buttons(10, 5, 'page_{number}')\n"
            "    .build()\n"
            ")\n"
            "await msg.reply('Navigate:', reply_markup=kb)"
        ),
        reply_markup=kb,
    )


async def _demo_hooks(callback: CallbackQuery) -> None:
    """Demonstrate ButtonValidator and validation hooks."""
    validator = ButtonValidator()
    good_btn = InlineButton(text="✅ Valid", callback_data="ok")
    bad_btn = InlineButton(text="a" * 100, callback_data="bad")

    good_result = validator.validate_button(good_btn)
    bad_result = validator.validate_button(bad_btn)
    is_valid = validate_button(good_btn)

    kb = InlineKeyboard()
    kb.row(InlineButton(text="⏪ Builder Menu", callback_data="menu:builder"))
    await callback.edit_message_text(
        "🪝 <b>Hooks & Validation</b>\n\n"
        f"<b>Good button:</b> valid={good_result['is_valid']}, "
        f"rules checked={good_result['checked_rules']}\n"
        f"<b>Bad button (100 chars):</b> valid={bad_result['is_valid']}, "
        f"errors={len(bad_result['errors'])}\n"
        f"<b>Convenience:</b> validate_button() → {is_valid}\n\n"
        "<b>Code to reproduce:</b>\n\n"
        + code_block(
            "from pykeyboard import ButtonValidator, validate_button\n\n"
            "validator = ButtonValidator()\n"
            "result = validator.validate_button(button)\n"
            "# {'is_valid': bool, 'errors': [...], 'checked_rules': int}\n\n"
            "# Or the convenience function:\n"
            "validate_button(button)  # → bool"
        ),
        reply_markup=kb,
    )


# ─── Error demo handlers ─────────────────────────────────────────────────────


async def _handle_error_demo(callback: CallbackQuery, error_type: str) -> None:
    """Trigger and display PyKeyboard errors with code snippets."""
    # Full report display
    if error_type.startswith("full_"):
        original = error_type.removeprefix("full_")
        await callback.edit_message_text(
            f"📋 <b>Full Error Report: {original.title()}</b>\n\n"
            "Full reports are available when errors occur.\n"
            "Check the terminal for the complete error log.\n\n"
            "<b>Code to reproduce:</b>\n\n"
            + code_block(
                "try:\n"
                "    # ... trigger an error ...\n"
                "except PyKeyboardError as e:\n"
                "    print(f'Code: {e.error_code}')\n"
                "    print(f'Message: {e.message}')\n"
                "    print(f'Full: {e}')  # formatted multi-line"
            ),
            reply_markup=error_menu_keyboard(),
        )
        return

    # Error trigger mapping
    trigger_code = {
        "pagination": "kb = InlineKeyboard()\nkb.paginate(0, 1, 'page_{number}')  # total_pages=0 → error",
        "duplicate": "kb = InlineKeyboard()\nkb.paginate(5, 3, 'page_{number}')  # first call\nkb.paginate(5, 3, 'page_{number}')  # duplicate → error",
        "locale": "kb = InlineKeyboard()\nkb.languages('invalid_pattern', ['en_US'])  # missing {locale}",
        "validation": "from pykeyboard.keyboard_base import Button\nButton(text='')  # empty text → error",
        "config": "kb = InlineKeyboard(row_width=0)  # invalid row_width → error",
    }

    try:
        match error_type:
            case "pagination":
                kb = InlineKeyboard()
                kb.paginate(0, 1, "page_{number}")
            case "duplicate":
                kb = InlineKeyboard()
                kb.paginate(5, 3, "page_{number}")
                kb.paginate(5, 3, "page_{number}")
            case "locale":
                kb = InlineKeyboard()
                kb.languages("invalid_pattern", ["en_US"])
            case "validation":
                from pykeyboard.keyboard_base import Button
                Button(text="")
            case "config":
                InlineKeyboard(row_width=0)
            case "help":
                kb = InlineKeyboard()
                kb.add(InlineButton(text="⏪ Error Menu", callback_data="menu:errors"))
                await callback.edit_message_text(
                    "🚨 <b>PyKeyboard Error Help</b>\n\n"
                    "Structured error handling:\n"
                    "• <code>error_code</code> — unique identifier\n"
                    "• <code>.param</code>, <code>.value</code>, <code>.reason</code> — context fields\n"
                    "• <code>str(e)</code> — clean formatted message\n"
                    "• All inherit from <code>PyKeyboardError</code>\n\n"
                    "<b>Code to reproduce:</b>\n\n"
                    + code_block(
                        "try:\n"
                        "    kb = InlineKeyboard(row_width=0)\n"
                        "except PyKeyboardError as e:\n"
                        "    print(e.error_code)  # 'CONFIGURATION_ERROR'\n"
                        "    print(e.message)     # human-readable message\n"
                        "    print(e.param)       # 'row_width'\n"
                        "    print(e.value)       # 0"
                    ),
                    reply_markup=kb,
                )
                return
            case _:
                await callback.answer(f"Unknown error type: {error_type}")
                return

    except PyKeyboardError as e:
        snippet = trigger_code.get(error_type, "# see error menu")
        response = (
            f"🚨 <b>PyKeyboard {type(e).__name__}</b>\n\n"
            f"<b>Error Code:</b> <code>{e.error_code}</code>\n"
            f"<b>Message:</b> {e.message}\n\n"
            "<b>Triggering code:</b>\n\n"
            + code_block(snippet)
        )
        kb = InlineKeyboard()
        kb.add(
            InlineButton(text="📋 Full Report", callback_data=f"error:full_{error_type}"),
            InlineButton(text="⏪ Error Menu", callback_data="menu:errors"),
        )
        await callback.edit_message_text(response, reply_markup=kb)

    except Exception as e:
        await callback.edit_message_text(
            f"🚨 <b>Unexpected Error</b>\n\n"
            f"<code>{type(e).__name__}: {e}</code>\n\n"
            "This error wasn't handled by PyKeyboard's error system.",
            reply_markup=error_menu_keyboard(),
        )


# ─── Action handlers ─────────────────────────────────────────────────────────


async def _handle_action(callback: CallbackQuery, action: str) -> None:
    """Handle inline button action callbacks."""
    if action == "url":
        kb = InlineKeyboard()
        kb.add(
            InlineButton(
                text="Open GitHub",
                url="https://github.com/johnnie-610/pykeyboard",
            )
        )
        kb.row(InlineButton(text="⏪ Main", callback_data="menu:main"))
        await callback.edit_message_text(
            "🔗 <b>URL Button</b>\n\n"
            "Open the project repository:\n\n"
            "<b>Code to reproduce:</b>\n\n"
            + code_block(
                "kb = InlineKeyboard()\n"
                "kb.add(InlineButton(\n"
                "    text='Open GitHub',\n"
                "    url='https://github.com/johnnie-610/pykeyboard',\n"
                "))\n"
                "await msg.reply('Visit us:', reply_markup=kb)"
            ),
            reply_markup=kb,
        )
    elif action == "close":
        await callback.edit_message_text(
            "✅ Closed.", reply_markup=main_menu_keyboard()
        )
    else:
        emoji_map = {
            "like": "👍", "dislike": "👎", "love": "❤️",
            "fire": "🔥", "star": "⭐",
        }
        emoji = emoji_map.get(action, "🎯")
        await callback.edit_message_text(
            f"{emoji} <b>Action:</b> {action}",
            reply_markup=main_menu_keyboard(),
        )


# ─── Message handlers ────────────────────────────────────────────────────────


@app.on_message()
async def on_message(_client: Client, message: Message):
    text = message.text or ""

    match text:
        case "❌ Remove Keyboard":
            rm = ReplyKeyboardRemove(selective=False)
            await message.reply_text("Keyboard removed.", reply_markup=rm)

        case "📝 Force Reply":
            fr = ForceReply(selective=True, placeholder="Please reply...")
            await message.reply_text(
                "Forcing reply to this message.", reply_markup=fr
            )

        case _ if text and not text.startswith("/"):
            await message.reply_text(
                "💬 <b>Message Received</b>\n"
                f"• Text length: {len(text)}\n"
                "• Use /start to open main menu"
            )


# ─── Entry point ──────────────────────────────────────────────────────────────


async def main():
    print("🤖 Starting PyKeyboard Showcase Bot")
    print("=" * 50)
    print(f"📚 Library: {LIBRARY_NAME}")
    print(f"🐍 Python: {PYTHON_VERSION}")
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
