# Utilities

Utility functions for creating and inspecting keyboards from configuration dicts.

Importable from `pykeyboard.utils`.

---

## create_keyboard_from_config <span class="api-badge method">function</span>

Create a keyboard from a configuration dictionary.

```python
create_keyboard_from_config(config: dict[str, Any]) -> InlineKeyboard | ReplyKeyboard
```

### Config Keys

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `type` | `str` | `"inline"` | `"inline"` or `"reply"` |
| `row_width` | `int` | — | Buttons per row |
| `buttons` | `list` | `[]` | Button configs (dicts or plain strings) |

!!! warning "Raises"
    **`ValueError`** — if `type` is not `"inline"` or `"reply"`

??? example "Usage"
    ```python
    from pykeyboard.utils import create_keyboard_from_config

    kb = create_keyboard_from_config({
        "type": "inline",
        "row_width": 2,
        "buttons": [
            {"text": "Yes", "callback_data": "yes"},
            {"text": "No", "callback_data": "no"},
        ],
    })
    ```

---

## get_keyboard_info <span class="api-badge method">function</span>

Get comprehensive metadata about a keyboard.

```python
get_keyboard_info(keyboard: InlineKeyboard | ReplyKeyboard) -> dict[str, Any]
```

### Return Fields

=== "Common"

    | Key | Type | Description |
    |-----|------|-------------|
    | `type` | `str` | Class name |
    | `row_width` | `int` | Row width |
    | `total_buttons` | `int` | Total buttons |
    | `total_rows` | `int` | Number of rows |

=== "InlineKeyboard extras"

    | Key | Type | Description |
    |-----|------|-------------|
    | `has_pagination` | `bool` | Has pagination |
    | `current_page` | `int` | Current page |
    | `total_pages` | `int` | Total pages |
    | `callback_pattern` | `str` | Callback pattern |
    | `custom_locales_count` | `int` | Custom locales count |

=== "ReplyKeyboard extras"

    | Key | Type | Description |
    |-----|------|-------------|
    | `is_persistent` | `bool` | Persistent keyboard |
    | `resize_keyboard` | `bool` | Auto-resize |
    | `one_time_keyboard` | `bool` | One-time use |
    | `selective` | `bool` | Selective display |
    | `placeholder` | `str` | Input placeholder |

??? example "Usage"
    ```python
    from pykeyboard import InlineKeyboard, InlineButton
    from pykeyboard.utils import get_keyboard_info

    kb = InlineKeyboard()
    kb.add(InlineButton("OK", "ok"))
    info = get_keyboard_info(kb)
    print(info["total_buttons"])  # 1
    ```

---

## validate_keyboard_config <span class="api-badge method">function</span>

Validate a configuration dict before creating a keyboard.

```python
validate_keyboard_config(config: dict[str, Any]) -> list[str]
```

**Returns:** List of error messages (empty if valid).

??? example "Usage"
    ```python
    from pykeyboard.utils import validate_keyboard_config

    errors = validate_keyboard_config({"type": "unknown", "row_width": -1})
    # ["Invalid keyboard type: unknown", "row_width must be a positive integer"]
    ```
