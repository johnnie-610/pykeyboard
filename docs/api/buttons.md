# Buttons

## Button <span class="api-badge class">Class</span>

Base button model with text validation. All button types inherit from this.

```python
Button(text: str)
```

!!! warning "Raises"
    **`ValidationError`** — if `text` is empty or whitespace-only

---

## InlineButton <span class="api-badge class">Class</span>

Inline keyboard button with full Pyrogram integration.

### Constructor

```python
InlineButton(
    text: str,
    callback_data: str | bytes | None = None,
    url: str | None = None,
    web_app: WebAppInfo | None = None,
    login_url: LoginUrl | None = None,
    user_id: int | None = None,
    switch_inline_query: str | None = None,
    switch_inline_query_current_chat: str | None = None,
    callback_game: CallbackGame | None = None,
    requires_password: bool | None = None,
    pay: bool | None = None,
    copy_text: str | None = None,
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Display text (required) |
| `callback_data` | `str \| bytes` | Data sent on press |
| `url` | `str` | URL to open |
| `web_app` | `WebAppInfo` | Web app to launch |
| `login_url` | `LoginUrl` | Authorization URL |
| `user_id` | `int` | Target user ID |
| `switch_inline_query` | `str` | Switch to inline mode |
| `switch_inline_query_current_chat` | `str` | Inline query in current chat |
| `callback_game` | `CallbackGame` | Game callback |
| `requires_password` | `bool` | Require password |
| `pay` | `bool` | Payment button |
| `copy_text` | `str` | Text to copy to clipboard |

!!! tip
    Only **one** action field should be set per button. The most common are `callback_data` and `url`.

### Methods

#### to_pyrogram <span class="api-badge method">method</span>

Convert to Pyrogram `InlineKeyboardButton`.

??? example "Usage"
    ```python
    from pykeyboard import InlineButton

    # Callback button
    btn = InlineButton("👍 Like", callback_data="like")

    # URL button
    link = InlineButton("🔗 Visit", url="https://example.com")

    # Contact button
    contact = InlineButton("📞 Support", user_id=123456)
    ```

---

## ReplyButton <span class="api-badge class">Class</span>

Reply keyboard button with device feature requests.

### Constructor

```python
ReplyButton(
    text: str,
    request_contact: bool | None = None,
    request_location: bool | None = None,
    request_poll: KeyboardButtonPollType | None = None,
    request_users: KeyboardButtonRequestUsers | None = None,
    request_chat: KeyboardButtonRequestChat | None = None,
    web_app: WebAppInfo | None = None,
)
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Display text (required) |
| `request_contact` | `bool` | Request phone number |
| `request_location` | `bool` | Request GPS location |
| `request_poll` | `KeyboardButtonPollType` | Request poll creation |
| `request_users` | `KeyboardButtonRequestUsers` | Request user selection |
| `request_chat` | `KeyboardButtonRequestChat` | Request chat selection |
| `web_app` | `WebAppInfo` | Web app to launch |

!!! tip
    Only **one** `request_*` field should be set per button.

### Methods

#### to_pyrogram <span class="api-badge method">method</span>

Convert to Pyrogram `KeyboardButton`.

??? example "Usage"
    ```python
    from pykeyboard import ReplyButton

    contact = ReplyButton("📞 Share Contact", request_contact=True)
    location = ReplyButton("📍 Share Location", request_location=True)
    ```
