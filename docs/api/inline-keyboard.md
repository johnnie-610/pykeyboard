# InlineKeyboard

<span class="api-badge class">Class</span>

Advanced inline keyboard with built-in pagination and 50+ language selection.

## Constructor

```python
InlineKeyboard(
    row_width: int = 3,
    callback_pattern: str = "",
    count_pages: int = 0,
    current_page: int = 0,
    custom_locales: dict[str, str] | None = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `row_width` | `int` | `3` | Buttons per row |
| `callback_pattern` | `str` | `""` | Pattern for callback data |
| `count_pages` | `int` | `0` | Total pages (pagination) |
| `current_page` | `int` | `0` | Current page number |
| `custom_locales` | `dict` | `None` | User-defined custom locales |

---

## Methods

### paginate <span class="api-badge method">method</span>

Create pagination keyboard with duplicate prevention and LRU caching.

```python
keyboard.paginate(
    count_pages: int,
    current_page: int,
    callback_pattern: str,
    source: str | None = None,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `count_pages` | `int` | Total pages (≥ 1) |
| `current_page` | `int` | Current page (≥ 1) |
| `callback_pattern` | `str` | Must contain `{number}` placeholder |
| `source` | `str \| None` | Source ID for multi-client isolation |

!!! warning "Raises"
    - **`PaginationError`** — invalid parameters
    - **`PaginationUnchangedError`** — identical keyboard already exists for this source

??? example "Usage"
    ```python
    from pykeyboard import InlineKeyboard, PaginationUnchangedError

    kb = InlineKeyboard()
    try:
        kb.paginate(10, 3, "page:{number}")
    except PaginationUnchangedError:
        pass  # keyboard unchanged
    ```

---

### languages <span class="api-badge method">method</span>

Create language selection keyboard with validation.

```python
keyboard.languages(
    callback_pattern: str,
    locales: str | list[str],
    row_width: int = 2,
)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `callback_pattern` | `str` | Must contain `{locale}` placeholder |
| `locales` | `str \| list[str]` | Locale code(s) to display |
| `row_width` | `int` | Buttons per row (≥ 1) |

!!! warning "Raises"
    **`LocaleError`** — invalid locale parameters

??? example "Usage"
    ```python
    kb = InlineKeyboard()
    kb.languages("lang:{locale}", ["en_US", "es_ES", "fr_FR"])
    ```

---

### add <span class="api-badge method">method</span>

Add buttons in rows based on `row_width`.

```python
keyboard.add(*buttons)
```

??? example "Usage"
    ```python
    kb = InlineKeyboard(row_width=2)
    kb.add(
        InlineButton("A", "a"),
        InlineButton("B", "b"),
        InlineButton("C", "c"),  # wraps to next row
    )
    ```

---

### row <span class="api-badge method">method</span>

Add a single row of buttons (ignores `row_width`).

```python
keyboard.row(*buttons)
```

---

### add_custom_locale <span class="api-badge method">method</span>

Register a custom locale for language keyboards.

```python
keyboard.add_custom_locale(locale_code: str, display_name: str)
```

??? example "Usage"
    ```python
    kb = InlineKeyboard()
    kb.add_custom_locale("en_PIRATE", "\U0001F3F4\u200D\u2620\uFE0F Pirate English")
    kb.languages("lang:{locale}", ["en_US", "en_PIRATE"])
    ```

---

### remove_custom_locale <span class="api-badge method">method</span>

Remove a custom locale. Returns `True` if removed, `False` if it didn't exist.

```python
keyboard.remove_custom_locale(locale_code: str) -> bool
```

---

### get_custom_locales <span class="api-badge method">method</span>

Get all custom locales defined on this keyboard.

**Returns:** `dict[str, str]` — locale codes → display names

---

### get_all_locales <span class="api-badge method">method</span>

Get all available locales (built-in + custom).

**Returns:** `dict[str, str]` — all locale codes → display names

---

### clear_pagination_hashes <span class="api-badge static">classmethod</span>

Clear stored pagination hashes for memory management.

```python
InlineKeyboard.clear_pagination_hashes(source: str | None = None) -> int
```

**Returns:** Number of hashes cleared.

---

### get_pagination_hash_stats <span class="api-badge static">classmethod</span>

Get statistics about stored pagination hashes.

**Returns:** `dict[str, Any]` with hash storage stats.

---

## Properties

### pyrogram_markup <span class="api-badge prop">property</span>

Get the Pyrogram `InlineKeyboardMarkup` for use with `reply_markup=`.

**Returns:** `InlineKeyboardMarkup`
