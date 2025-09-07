# Buttons API Reference

## Class: Button

Base button model with text validation.

### Constructor

```python
Button(text: str)
```

### Attributes

- `text` (str): The display text for the button. Must be a non-empty string.

### Validation

- Text cannot be empty or whitespace-only
- Raises `ValidationError` if validation fails

---

## Class: InlineButton

Inline keyboard button with comprehensive Pyrogram integration.

### Constructor

```python
InlineButton(
    text: str,
    callback_data: Optional[Union[str, bytes]] = None,
    url: Optional[str] = None,
    web_app: Optional[WebAppInfo] = None,
    login_url: Optional[LoginUrl] = None,
    user_id: Optional[int] = None,
    switch_inline_query: Optional[str] = None,
    switch_inline_query_current_chat: Optional[str] = None,
    callback_game: Optional[CallbackGame] = None,
    requires_password: Optional[bool] = None,
    pay: Optional[bool] = None,
    copy_text: Optional[str] = None
)
```

### Attributes

- `text` (str): Button display text (inherited from Button)
- `callback_data` (Optional[Union[str, bytes]]): Callback data sent when button is pressed
- `url` (Optional[str]): URL to open when button is pressed
- `web_app` (Optional[WebAppInfo]): Web app to open
- `login_url` (Optional[LoginUrl]): Login URL for authorization
- `user_id` (Optional[int]): User ID for the button
- `switch_inline_query` (Optional[str]): Switch to inline query
- `switch_inline_query_current_chat` (Optional[str]): Switch to inline query in current chat
- `callback_game` (Optional[CallbackGame]): Callback game
- `requires_password` (Optional[bool]): Whether password is required
- `pay` (Optional[bool]): Whether this is a pay button
- `copy_text` (Optional[str]): Text to copy to clipboard

### Methods

#### to_pyrogram()

Convert to Pyrogram InlineKeyboardButton.

**Returns:**
- `InlineKeyboardButton`: Pyrogram-compatible button instance

### Notes

- Only one of the optional fields should be used per button for optimal UX
- Supports both positional and keyword arguments (positional deprecated)

---

## Class: ReplyButton

Reply keyboard button with comprehensive Pyrogram integration and advanced features.

### Constructor

```python
ReplyButton(
    text: str,
    request_contact: Optional[bool] = None,
    request_location: Optional[bool] = None,
    request_poll: Optional[KeyboardButtonPollType] = None,
    request_users: Optional[KeyboardButtonRequestUsers] = None,
    request_chat: Optional[KeyboardButtonRequestChat] = None,
    web_app: Optional[WebAppInfo] = None
)
```

### Attributes

- `text` (str): Button display text (inherited from Button)
- `request_contact` (Optional[bool]): Request user's contact information when pressed
- `request_location` (Optional[bool]): Request user's location when pressed
- `request_poll` (Optional[KeyboardButtonPollType]): Request poll creation with specified type
- `request_users` (Optional[KeyboardButtonRequestUsers]): Request user selection with specified criteria
- `request_chat` (Optional[KeyboardButtonRequestChat]): Request chat selection with specified criteria
- `web_app` (Optional[WebAppInfo]): Web app to open when button is pressed

### Methods

#### to_pyrogram()

Convert to Pyrogram KeyboardButton.

**Returns:**
- `KeyboardButton`: Pyrogram-compatible button instance

### Notes

- Only one request_* field should be set per button for optimal UX
- Supports both positional and keyword arguments (positional deprecated)