# ReplyKeyboard API Reference

## Class: ReplyKeyboard

Reply keyboard with comprehensive Pyrogram integration and customization options.

### Constructor

```python
ReplyKeyboard(
    row_width: int = 3,
    is_persistent: Optional[bool] = None,
    resize_keyboard: Optional[bool] = None,
    one_time_keyboard: Optional[bool] = None,
    selective: Optional[bool] = None,
    placeholder: Optional[str] = None
)
```

### Attributes

- `row_width` (int): Number of buttons per row (default: 3)
- `is_persistent` (Optional[bool]): Whether the keyboard is persistent
- `resize_keyboard` (Optional[bool]): Whether to resize the keyboard
- `one_time_keyboard` (Optional[bool]): Whether it's a one-time keyboard
- `selective` (Optional[bool]): Whether the keyboard is selective
- `placeholder` (Optional[str]): Placeholder text for the input field

### Methods

#### add(*args)

Add buttons to keyboard in rows based on row_width.

**Parameters:**
- `*args`: Variable number of buttons or button-like objects to add

#### row(*args)

Add a new row of buttons to the keyboard.

**Parameters:**
- `*args`: Variable number of buttons to add as a single row

#### to_dict()

Convert keyboard to dictionary representation for serialization.

**Returns:**
- `dict`: Dictionary representation of the keyboard

#### from_dict(data)

Create keyboard instance from dictionary representation.

**Parameters:**
- `data` (dict): Dictionary representation of a keyboard

**Returns:**
- `ReplyKeyboard`: Reconstructed keyboard instance

#### to_json()

Convert keyboard to JSON string.

**Returns:**
- `str`: JSON representation of the keyboard

#### from_json(json_str)

Create keyboard instance from JSON string.

**Parameters:**
- `json_str` (str): JSON string representation of a keyboard

**Returns:**
- `ReplyKeyboard`: Reconstructed keyboard instance

### Properties

#### pyrogram_markup

Get the Pyrogram ReplyKeyboardMarkup for this keyboard.

**Returns:**
- `ReplyKeyboardMarkup`: Pyrogram-compatible markup

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

- `text` (str): Button display text
- `request_contact` (Optional[bool]): Request contact information
- `request_location` (Optional[bool]): Request location information
- `request_poll` (Optional[KeyboardButtonPollType]): Request poll
- `request_users` (Optional[KeyboardButtonRequestUsers]): Request users
- `request_chat` (Optional[KeyboardButtonRequestChat]): Request chat
- `web_app` (Optional[WebAppInfo]): Web app to open

### Methods

#### to_pyrogram()

Convert to Pyrogram KeyboardButton.

**Returns:**
- `KeyboardButton`: Pyrogram-compatible button instance

---

## Class: PyReplyKeyboardRemove

Remove reply keyboard markup with selective option.

### Constructor

```python
PyReplyKeyboardRemove(selective: Optional[bool] = None)
```

### Attributes

- `selective` (Optional[bool]): Whether the removal should be selective

### Methods

#### to_pyrogram()

Convert to Pyrogram ReplyKeyboardRemove.

**Returns:**
- `ReplyKeyboardRemove`: Pyrogram-compatible remove markup

---

## Class: PyForceReply

Force user to send a reply with selective and placeholder options.

### Constructor

```python
PyForceReply(
    selective: Optional[bool] = None,
    placeholder: Optional[str] = None
)
```

### Attributes

- `selective` (Optional[bool]): Whether the force reply should be selective
- `placeholder` (Optional[str]): Placeholder text shown in the input field

### Methods

#### to_pyrogram()

Convert to Pyrogram ForceReply.

**Returns:**
- `ForceReply`: Pyrogram-compatible force reply markup