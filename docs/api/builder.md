# Builder API Reference

## Class: KeyboardBuilder

Fluent API builder for type-safe keyboard construction.

### Constructor

```python
KeyboardBuilder(keyboard: Union[InlineKeyboard, ReplyKeyboard])
```

### Methods

#### add_validation_hook(hook)

Add a validation hook that runs before adding buttons.

**Parameters:**
- `hook` (Callable[[Any], bool]): Function that takes a button and returns True if valid

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_button_transform(transform)

Add a button transformation function.

**Parameters:**
- `transform` (Callable[[Any], Any]): Function that takes a button and returns transformed button

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_button(text, callback_data=None, **kwargs)

Add a single button to the keyboard.

**Parameters:**
- `text` (str): Button text
- `callback_data` (Optional[str]): Callback data (for inline keyboards)
- `**kwargs`: Additional button parameters

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_buttons(*buttons)

Add multiple buttons at once.

**Parameters:**
- `*buttons` (Union[str, Dict[str, Any], Any]): Button specifications (strings, dicts, or button objects)

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_row(*buttons)

Add a complete row of buttons.

**Parameters:**
- `*buttons` (Union[str, Dict[str, Any], Any]): Button specifications for the row

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_conditional_button(condition, text, callback_data=None, **kwargs)

Add a button only if condition is True.

**Parameters:**
- `condition` (bool): Whether to add the button
- `text` (str): Button text
- `callback_data` (Optional[str]): Callback data
- `**kwargs`: Additional button parameters

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_paginated_buttons(items, callback_pattern, items_per_page=5, current_page=1)

Add paginated buttons from a list of items.

**Parameters:**
- `items` (List[str]): List of item texts
- `callback_pattern` (str): Pattern for callback data with {item} and {page} placeholders
- `items_per_page` (int): Number of items per page
- `current_page` (int): Current page number

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_navigation_buttons(total_pages, current_page, callback_pattern="page_{number}")

Add navigation buttons for pagination.

**Parameters:**
- `total_pages` (int): Total number of pages
- `current_page` (int): Current page number
- `callback_pattern` (str): Pattern for callback data

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### add_language_buttons(locales, callback_pattern="lang_{locale}", row_width=2)

Add language selection buttons.

**Parameters:**
- `locales` (List[str]): List of locale codes
- `callback_pattern` (str): Pattern for callback data
- `row_width` (int): Number of buttons per row

**Returns:**
- `KeyboardBuilder`: Self for method chaining

#### build()

Build and return the final keyboard.

**Returns:**
- `Union[InlineKeyboard, ReplyKeyboard]`: The constructed keyboard

---

## Class: KeyboardFactory

Factory class for creating keyboards with predefined configurations.

### Methods

#### create_confirmation_keyboard(yes_text="✅ Yes", no_text="❌ No", cancel_text=None, callback_pattern="confirm_{action}", columns=2)

Create a confirmation dialog keyboard.

**Parameters:**
- `yes_text` (str): Text for yes button
- `no_text` (str): Text for no button
- `cancel_text` (Optional[str]): Text for cancel button (optional)
- `callback_pattern` (str): Pattern for callback data
- `columns` (int): Row width of the keyboard

**Returns:**
- `InlineKeyboard`: Configured InlineKeyboard

#### create_menu_keyboard(menu_items, callback_pattern="menu_{action}", columns=2)

Create a menu keyboard from a dictionary of items.

**Parameters:**
- `menu_items` (Dict[str, str]): Dict mapping button text to action
- `callback_pattern` (str): Pattern for callback data
- `columns` (int): Number of columns

**Returns:**
- `InlineKeyboard`: Configured InlineKeyboard

#### create_rating_keyboard(max_rating=5, callback_pattern="rate_{stars}", include_labels=True)

Create a star rating keyboard.

**Parameters:**
- `max_rating` (int): Maximum rating value
- `callback_pattern` (str): Pattern for callback data
- `include_labels` (bool): Whether to include rating labels

**Returns:**
- `InlineKeyboard`: Configured InlineKeyboard

#### create_pagination_keyboard(total_pages, current_page, callback_pattern="page_{number}", include_buttons=None)

Create a pagination keyboard with optional additional buttons.

**Parameters:**
- `total_pages` (int): Total number of pages
- `current_page` (int): Current page number
- `callback_pattern` (str): Pattern for pagination callbacks
- `include_buttons` (Optional[List[Dict[str, str]]]): Additional buttons to include

**Returns:**
- `InlineKeyboard`: Configured InlineKeyboard

#### create_language_keyboard(locales, callback_pattern="lang_{locale}", row_width=2)

Create a language selection keyboard.

**Parameters:**
- `locales` (List[str]): List of locale codes
- `callback_pattern` (str): Pattern for callback data
- `row_width` (int): Number of buttons per row

**Returns:**
- `InlineKeyboard`: Configured InlineKeyboard

#### clone_keyboard(source_keyboard, deep_copy=True)

Clone an existing keyboard.

**Parameters:**
- `source_keyboard` (Union[InlineKeyboard, ReplyKeyboard]): Keyboard to clone
- `deep_copy` (bool): Whether to perform deep copy

**Returns:**
- `Union[InlineKeyboard, ReplyKeyboard]`: Cloned keyboard instance

---

## Functions

### build_inline_keyboard()

Create a builder for inline keyboards.

**Returns:**
- `KeyboardBuilder`: Builder instance for InlineKeyboard

### build_reply_keyboard()

Create a builder for reply keyboards.

**Returns:**
- `KeyboardBuilder`: Builder instance for ReplyKeyboard

---

## Decorators

### keyboard_factory(func)

Decorator to mark functions as keyboard factories.

**Parameters:**
- `func` (Callable): Function to decorate

**Returns:**
- `Callable`: Decorated function with additional validation and error handling