# Builder & Factory

## KeyboardBuilder <span class="api-badge class">Class</span>

Fluent API for constructing keyboards with method chaining.

### Constructor

```python
KeyboardBuilder(keyboard: InlineKeyboard | ReplyKeyboard)
```

---

### add_button <span class="api-badge method">method</span>

Add a single button.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | `str` | — | Button text |
| `callback_data` | `str \| None` | `None` | Callback data (inline only) |
| `**kwargs` | | | Additional button parameters |

**Returns:** `KeyboardBuilder` (chainable)

---

### add_buttons <span class="api-badge method">method</span>

Add multiple buttons at once.

```python
builder.add_buttons(*buttons)
```

Accepts strings, dicts with button params, or button objects.

**Returns:** `KeyboardBuilder` (chainable)

---

### add_row <span class="api-badge method">method</span>

Add a complete row of buttons.

```python
builder.add_row(*buttons)
```

**Returns:** `KeyboardBuilder` (chainable)

??? example "Fluent Example"
    ```python
    from pykeyboard import KeyboardBuilder, InlineKeyboard

    kb = (
        KeyboardBuilder(InlineKeyboard())
        .add_row("✅ Yes", "❌ No")
        .add_row("🤔 Maybe", "⏪ Cancel")
        .build()
    )
    ```

---

### add_conditional_button <span class="api-badge method">method</span>

Add a button only if a condition is `True`.

| Parameter | Type | Description |
|-----------|------|-------------|
| `condition` | `bool` | Whether to add the button |
| `text` | `str` | Button text |
| `callback_data` | `str \| None` | Callback data |

**Returns:** `KeyboardBuilder` (chainable)

??? example "Usage"
    ```python
    is_admin = user.is_admin
    kb = (
        KeyboardBuilder(InlineKeyboard())
        .add_row("📊 Dashboard")
        .add_conditional_button(is_admin, "🔧 Admin Panel", "admin")
        .build()
    )
    ```

---

### add_navigation_buttons <span class="api-badge method">method</span>

Add pagination navigation buttons.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `total_pages` | `int` | — | Total pages |
| `current_page` | `int` | — | Current page |
| `callback_pattern` | `str` | `"page_{number}"` | Callback pattern |

**Returns:** `KeyboardBuilder` (chainable)

---

### add_language_buttons <span class="api-badge method">method</span>

Add language selection buttons.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `locales` | `list[str]` | — | Locale codes |
| `callback_pattern` | `str` | `"lang_{locale}"` | Callback pattern |
| `row_width` | `int` | `2` | Buttons per row |

**Returns:** `KeyboardBuilder` (chainable)

---

### add_validation_hook <span class="api-badge method">method</span>

Add a validation hook that runs before adding buttons.

**Returns:** `KeyboardBuilder` (chainable)

---

### add_button_transform <span class="api-badge method">method</span>

Add a button transformation function.

**Returns:** `KeyboardBuilder` (chainable)

---

### build <span class="api-badge method">method</span>

Build and return the final keyboard.

**Returns:** `InlineKeyboard | ReplyKeyboard`

---

## KeyboardFactory <span class="api-badge class">Class</span>

One-line factory methods for common keyboard patterns.

### create_confirmation_keyboard <span class="api-badge static">static</span>

```python
KeyboardFactory.create_confirmation_keyboard(
    yes_text: str = "✅ Yes",
    no_text: str = "❌ No",
    cancel_text: str | None = None,
    callback_pattern: str = "confirm_{action}",
    columns: int = 2,
) -> InlineKeyboard
```

??? example "Usage"
    ```python
    kb = KeyboardFactory.create_confirmation_keyboard(
        yes_text="✅ Confirm Order",
        no_text="❌ Cancel",
        callback_pattern="order_{action}",
    )
    ```

---

### create_menu_keyboard <span class="api-badge static">static</span>

```python
KeyboardFactory.create_menu_keyboard(
    menu_items: dict[str, str],
    callback_pattern: str = "menu_{action}",
    columns: int = 2,
) -> InlineKeyboard
```

??? example "Usage"
    ```python
    kb = KeyboardFactory.create_menu_keyboard({
        "🏠 Home": "home",
        "⚙️ Settings": "settings",
        "ℹ️ Help": "help",
    })
    ```

---

### create_rating_keyboard <span class="api-badge static">static</span>

```python
KeyboardFactory.create_rating_keyboard(
    max_rating: int = 5,
    callback_pattern: str = "rate_{stars}",
    include_labels: bool = True,
) -> InlineKeyboard
```

---

### create_pagination_keyboard <span class="api-badge static">static</span>

```python
KeyboardFactory.create_pagination_keyboard(
    total_pages: int,
    current_page: int,
    callback_pattern: str = "page_{number}",
    include_buttons: list[dict[str, str]] | None = None,
) -> InlineKeyboard
```

---

### create_language_keyboard <span class="api-badge static">static</span>

```python
KeyboardFactory.create_language_keyboard(
    locales: list[str],
    callback_pattern: str = "lang_{locale}",
    row_width: int = 2,
) -> InlineKeyboard
```

---

### clone_keyboard <span class="api-badge static">static</span>

Clone an existing keyboard (deep or shallow copy).

```python
KeyboardFactory.clone_keyboard(
    source_keyboard: InlineKeyboard | ReplyKeyboard,
    deep_copy: bool = True,
) -> InlineKeyboard | ReplyKeyboard
```

---

!!! note "Removed APIs"
    The `keyboard_factory` decorator and standalone `build_inline_keyboard()` / `build_reply_keyboard()` functions have been removed. Use `KeyboardBuilder(InlineKeyboard())` and `KeyboardBuilder(ReplyKeyboard())` directly.
