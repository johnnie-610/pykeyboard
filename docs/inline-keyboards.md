# Inline Keyboards

Inline keyboards are the most powerful feature of PyKeyboard, providing rich interactive experiences for your Telegram bots.

## Basic Usage

```python
from pykeyboard import InlineKeyboard, InlineButton

# Create keyboard
keyboard = InlineKeyboard()

# Add buttons
keyboard.add(
    InlineButton("Option 1", "choice:1"),
    InlineButton("Option 2", "choice:2"),
    InlineButton("Cancel", "action:cancel")
)

# Send to user
await message.reply_text("Choose an option:", reply_markup=keyboard)
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/add_inline_button.png" alt="Add Inline Buttons">
<figcaption><em>Example of inline keyboard with added buttons</em></figcaption>
</figure>

## Button Types

### Text Buttons

```python
InlineButton("Click me", "callback_data")
```

### URL Buttons

```python
InlineButton("Visit Website", url="https://example.com")
```

### Web App Buttons

```python
from pyrogram.types import WebAppInfo

button = InlineButton("Open Web App", web_app=WebAppInfo(url="https://myapp.com"))
```

### Login Buttons

```python
from pyrogram.types import LoginUrl

button = InlineButton("Login", login_url=LoginUrl(url="https://example.com/login"))
```

## Layout Control

### Row Width

```python
# 2 buttons per row
keyboard = InlineKeyboard(row_width=2)
keyboard.add("A", "B", "C", "D")  # Creates 2 rows: [A,B], [C,D]
```

### Manual Rows

```python
keyboard = InlineKeyboard()
keyboard.row("Button 1", "Button 2")  # First row
keyboard.row("Button 3")              # Second row
keyboard.add("Button 4", "Button 5")  # Third row (auto-layout)
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/row_inline_button.png" alt="Row Inline Buttons">
<figcaption><em>Example of inline keyboard with row-based layout</em></figcaption>
</figure>

## Advanced Features

### Pagination

```python
keyboard = InlineKeyboard()
keyboard.paginate(
    count_pages=25,
    current_page=12,
    callback_pattern="page:{number}"
)
# Creates: « 1 ‹ 11 · 12 · 13 › 25 »
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_25.png" alt="Pagination Keyboard 25 Pages">
<figcaption><em>Pagination with 25 pages, current page 14</em></figcaption>
</figure>

#### Different Page Counts

**3 Pages:**

```python
keyboard = InlineKeyboard()
keyboard.paginate(3, 2, 'pagination:{number}')
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_3.png" alt="Pagination Keyboard 3 Pages">
<figcaption><em>Pagination with 3 pages, current page 3</em></figcaption>
</figure>

**5 Pages:**

```python
keyboard = InlineKeyboard()
keyboard.paginate(5, 3, 'pagination:{number}')
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_5.png" alt="Pagination Keyboard 5 Pages">
<figcaption><em>Pagination with 5 pages, current page 3</em></figcaption>
</figure>

**9 Pages:**

```python
keyboard = InlineKeyboard()
keyboard.paginate(9, 5, 'pagination:{number}')
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_9.png" alt="Pagination Keyboard 9 Pages">
<figcaption><em>Pagination with 9 pages, current page 5</em></figcaption>
</figure>

**100 Pages:**

```python
keyboard = InlineKeyboard()
keyboard.paginate(100, 50, 'page:{number}')
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_100.png" alt="Pagination Keyboard 100 Pages">
<figcaption><em>Pagination with 100 pages, current page 100</em></figcaption>
</figure>

**150 Pages with Additional Buttons:**

```python
keyboard = InlineKeyboard()
keyboard.paginate(150, 75, 'page:{number}')
keyboard.row(
    InlineButton('🔙 Back', 'action:back'),
    InlineButton('❌ Close', 'action:close')
)
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/pagination_keyboard_150.png" alt="Pagination Keyboard 150 Pages">
<figcaption><em>Pagination with 150 pages and additional action buttons</em></figcaption>
</figure>

### Language Selection

```python
keyboard = InlineKeyboard()
keyboard.languages(
    callback_pattern="lang:{locale}",
    locales=["en_US", "es_ES", "fr_FR", "de_DE"],
    row_width=2
)
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/languages_keyboard.png" alt="Language Selection Keyboard">
<figcaption><em>Language selection keyboard with multiple locales</em></figcaption>
</figure>

### Builder Pattern

```python
from pykeyboard import KeyboardBuilder, InlineKeyboard

keyboard = (
    KeyboardBuilder(InlineKeyboard())
    .add_row("✅ Yes", "❌ No")
    .add_row("🤔 Maybe", "⏪ Cancel")
    .build()
)
```

## Best Practices

### Callback Data Patterns

```python
# Good: Structured callback data
InlineButton("Edit", "action:edit:item:123")

# Bad: Unstructured data
InlineButton("Edit", "edit_item_123")
```

### Error Handling

```python
from pykeyboard import PaginationUnchangedError

try:
    await callback_query.edit_message_text("Updated!")
except PaginationUnchangedError as e:
    # Handle MessageNotModifiedError, etc.
    await callback_query.answer("Already updated")
```

## Common Patterns

### Confirmation Dialog

```python
from pykeyboard import KeyboardFactory

keyboard = KeyboardFactory.create_confirmation_keyboard(
    yes_text="✅ Confirm",
    no_text="❌ Cancel",
    callback_pattern="confirm:{action}"
)
```

### Menu Navigation

```python
def create_menu(items, callback_prefix):
    keyboard = InlineKeyboard(row_width=2)
    for item in items:
        keyboard.add(InlineButton(item['name'], f"{callback_prefix}:{item['id']}"))
    return keyboard
```

### Dynamic Updates

```python
@app.on_callback_query(filters.regex(r"counter:(\w+)"))
async def handle_counter(client, callback_query):
    action = callback_query.matches[0].group(1)

    # Update counter in database
    new_count = update_counter(action)

    # Update keyboard with new data
    keyboard = create_counter_keyboard(new_count)
    await callback_query.edit_message_reply_markup(keyboard)
```

## Troubleshooting

### PaginationUnchangedError

```python
keyboard.paginate(5, 1, "page:{number}", "user_123")  # Safe to call multiple times
```

### Callback Timeout

```python
# Always answer callbacks quickly
await callback_query.answer()  # Answer immediately

# Then do heavy processing
await do_heavy_work()

# Finally update message
await callback_query.edit_message_text("Done!")
```
