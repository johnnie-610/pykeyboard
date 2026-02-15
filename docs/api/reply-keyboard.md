# ReplyKeyboard

<span class="api-badge class">Class</span>

Reply keyboard with full Pyrogram integration and customization options.

## Constructor

```python
ReplyKeyboard(
    row_width: int = 3,
    is_persistent: bool | None = None,
    resize_keyboard: bool | None = None,
    one_time_keyboard: bool | None = None,
    selective: bool | None = None,
    placeholder: str | None = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `row_width` | `int` | `3` | Buttons per row |
| `is_persistent` | `bool \| None` | `None` | Keep keyboard visible |
| `resize_keyboard` | `bool \| None` | `None` | Resize to fit content |
| `one_time_keyboard` | `bool \| None` | `None` | Hide after one use |
| `selective` | `bool \| None` | `None` | Show only to specific users |
| `placeholder` | `str \| None` | `None` | Input field placeholder text |

!!! warning "Raises"
    **`ConfigurationError`** — if `row_width` < 1

---

## Methods

### add <span class="api-badge method">method</span>

Add buttons in rows based on `row_width`.

```python
keyboard.add(*buttons)
```

??? example "Usage"
    ```python
    from pykeyboard import ReplyKeyboard, ReplyButton

    kb = ReplyKeyboard(row_width=2, resize_keyboard=True)
    kb.add(
        ReplyButton("📞 Share Contact", request_contact=True),
        ReplyButton("📍 Share Location", request_location=True),
    )
    ```

---

### row <span class="api-badge method">method</span>

Add a single explicit row of buttons (ignores `row_width`).

```python
keyboard.row(*buttons)
```

---

## Properties

### pyrogram_markup <span class="api-badge prop">property</span>

Get the Pyrogram `ReplyKeyboardMarkup` for use with `reply_markup=`.

**Returns:** `ReplyKeyboardMarkup`

---

## Related Classes

### PyReplyKeyboardRemove <span class="api-badge class">Class</span>

Remove reply keyboard markup.

```python
PyReplyKeyboardRemove(selective: bool | None = None)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `to_pyrogram()` | `ReplyKeyboardRemove` | Pyrogram-compatible markup |

??? example "Usage"
    ```python
    from pykeyboard import PyReplyKeyboardRemove

    await message.reply("Keyboard removed", reply_markup=PyReplyKeyboardRemove())
    ```

---

### PyForceReply <span class="api-badge class">Class</span>

Force the user to send a reply.

```python
PyForceReply(
    selective: bool | None = None,
    placeholder: str | None = None,
)
```

| Method | Returns | Description |
|--------|---------|-------------|
| `to_pyrogram()` | `ForceReply` | Pyrogram-compatible markup |

??? example "Usage"
    ```python
    from pykeyboard import PyForceReply

    await message.reply("Your name?", reply_markup=PyForceReply(placeholder="Type here..."))
    ```
