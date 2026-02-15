# Reply Keyboards

Reply keyboards are shown at the bottom of the chat interface and allow users to send predefined responses by tapping buttons.

## Basic Usage

```python
from pykeyboard import ReplyKeyboard, ReplyButton

# Create a simple reply keyboard
keyboard = ReplyKeyboard()
keyboard.add(
    ReplyButton("Yes"),
    ReplyButton("No"),
    ReplyButton("Maybe")
)

# Use with your bot
await message.reply_text("What do you think?", reply_markup=keyboard)
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/add_reply_button.png"Add Reply Buttons">
<figcaption>Example of reply keyboard with added buttons</figcaption>
</figure>

## Parameters

- `row_width` (int, default 3): Number of buttons per row
- `resize_keyboard` (bool, optional): Whether to resize keyboard to fit content
- `one_time_keyboard` (bool, optional): Whether keyboard disappears after one use
- `selective` (bool, optional): Whether keyboard is shown only to specific users
- `placeholder` (str, optional): Placeholder text shown in input field

## Advanced Features

### Contact and Location Requests

```python
keyboard = ReplyKeyboard(resize_keyboard=True)
keyboard.row(
    ReplyButton("📱 Share Contact", request_contact=True),
    ReplyButton("📍 Share Location", request_location=True)
)
keyboard.row(ReplyButton("❌ Cancel"))
```

### Poll Creation

```python
keyboard = ReplyKeyboard()
keyboard.add(
    ReplyButton("📊 Create Quiz", request_poll=KeyboardButtonPollType(type="quiz")),
    ReplyButton("📈 Create Poll", request_poll=KeyboardButtonPollType(type="regular"))
)
```

### User and Chat Selection

```python
from pyrogram.types import KeyboardButtonRequestUsers, KeyboardButtonRequestChat

keyboard = ReplyKeyboard()
keyboard.add(
    ReplyButton("👤 Select User", request_users=KeyboardButtonRequestUsers(request_id=1)),
    ReplyButton("👥 Select Chat", request_chat=KeyboardButtonRequestChat(request_id=2))
)
```

### Web App Integration

```python
from pyrogram.types import WebAppInfo

keyboard = ReplyKeyboard()
keyboard.add(
    ReplyButton("🌐 Open Web App", web_app=WebAppInfo(url="https://example.com"))
)
```

## Layout Control

### Row-based Layout

```python
keyboard = ReplyKeyboard()
keyboard.row(ReplyButton("Top Button"))
keyboard.row(
    ReplyButton("Left"),
    ReplyButton("Right")
)
keyboard.row(ReplyButton("Bottom Button"))
```

<figure html>
<img src="https://raw.githubusercontent.com/johnnie-610/pykeyboard/main/docs/source/images/row_reply_button.png" alt="Row Reply Buttons">
<figcaption>Example of reply keyboard with row-based layout</figcaption>
</figure>

### Automatic Layout

```python
keyboard = ReplyKeyboard(row_width=2)
keyboard.add(
    ReplyButton("Button 1"),
    ReplyButton("Button 2"),
    ReplyButton("Button 3"),
    ReplyButton("Button 4"),
    ReplyButton("Button 5")  # Will be on its own row
)
```

## Keyboard Types

### One-time Keyboard

```python
keyboard = ReplyKeyboard(
    one_time_keyboard=True,
    placeholder="Choose an option..."
)
keyboard.add(ReplyButton("Option 1"), ReplyButton("Option 2"))
```

### Resizable Keyboard

```python
keyboard = ReplyKeyboard(resize_keyboard=True)
keyboard.add(ReplyButton("Small Button"))
```

### Selective Keyboard

```python
keyboard = ReplyKeyboard(selective=True)
keyboard.add(ReplyButton("For You Only"))
```

## Integration Examples

### Complete Bot Example

```python
from pyrogram import Client, filters
from pykeyboard import ReplyKeyboard, ReplyButton

app = Client("my_bot")

# Main menu keyboard
main_menu = ReplyKeyboard(resize_keyboard=True, one_time_keyboard=True)
main_menu.add(
    ReplyButton("📋 Tasks"),
    ReplyButton("📊 Statistics"),
    ReplyButton("⚙️ Settings")
)

# Settings keyboard
settings_menu = ReplyKeyboard(resize_keyboard=True)
settings_menu.row(
    ReplyButton("🔔 Notifications"),
    ReplyButton("🌐 Language")
)
settings_menu.row(ReplyButton("⬅️ Back"))

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Welcome! Choose an option:",
        reply_markup=main_menu
    )

@app.on_message(filters.text & filters.regex("Settings"))
async def settings_handler(client, message):
    await message.reply_text(
        "Settings:",
        reply_markup=settings_menu
    )

app.run()
```

### Contact Collection

```python
contact_keyboard = ReplyKeyboard(resize_keyboard=True)
contact_keyboard.row(
    ReplyButton("📱 Share Contact", request_contact=True)
)
contact_keyboard.row(ReplyButton("Skip"))

@app.on_message(filters.contact)
async def contact_handler(client, message):
    contact = message.contact
    await message.reply_text(f"Thanks! Phone: {contact.phone_number}")

@app.on_message(filters.text & filters.regex("Share Contact"))
async def request_contact(client, message):
    await message.reply_text(
        "Please share your contact:",
        reply_markup=contact_keyboard
    )
```

## Best Practices

1. **Use appropriate keyboard types**: One-time keyboards for menus, persistent for ongoing interactions
2. **Keep it simple**: Don't overload users with too many options
3. **Use emojis**: They make buttons more recognizable
4. **Handle all responses**: Make sure your bot can handle all possible button presses
5. **Consider mobile**: Test on mobile devices as button layout may differ

## Error Handling

```python
from pykeyboard import ConfigurationError

try:
    keyboard = ReplyKeyboard(row_width=0)  # Invalid
except ConfigurationError as e:
    print(f"Error code: {e.error_code}")
    print(f"Parameter: {e.param}")  # "row_width"
    print(f"Value: {e.value}")      # 0
```
