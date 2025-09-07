# InlineKeyboard API Reference

## Class: InlineKeyboard

Advanced inline keyboard with pagination and language selection support.

### Constructor

```python
InlineKeyboard(
    row_width: int = 3,
    callback_pattern: str = "",
    count_pages: int = 0,
    current_page: int = 0,
    custom_locales: Dict[str, str] = None
)
```

### Attributes

- `row_width` (int): Number of buttons per row (default: 3)
- `callback_pattern` (str): Pattern for callback data
- `count_pages` (int): Total number of pages
- `current_page` (int): Current page number
- `custom_locales` (Dict[str, str]): User-defined custom locales

### Methods

#### paginate(count_pages, current_page, callback_pattern, source=None)

Create pagination keyboard with comprehensive edge case handling and automatic duplicate prevention.

**Parameters:**
- `count_pages` (int): Total number of pages. Must be >= 1.
- `current_page` (int): The page number currently being viewed. Must be >= 1.
- `callback_pattern` (str): The pattern used for callback data. Must contain '{number}' placeholder.
- `source` (Optional[str]): Source identifier for isolation in multi-client scenarios.

**Raises:**
- `PaginationError`: If pagination parameters are invalid.
- `PaginationUnchangedError`: If identical keyboard was already created for this source.

#### languages(callback_pattern, locales, row_width=2)

Create language selection keyboard with comprehensive validation.

**Parameters:**
- `callback_pattern` (str): Pattern for callback data with {locale} placeholder.
- `locales` (Union[str, List[str]]): Single locale string or list of locale codes.
- `row_width` (int): Number of buttons per row. Must be >= 1.

**Raises:**
- `LocaleError`: If locale parameters are invalid.

#### add_custom_locale(locale_code, display_name)

Add a custom locale to the keyboard's locale dictionary.

**Parameters:**
- `locale_code` (str): The locale code (e.g., 'en_CUSTOM')
- `display_name` (str): The display name with flag emoji

#### remove_custom_locale(locale_code)

Remove a custom locale from the keyboard.

**Parameters:**
- `locale_code` (str): The locale code to remove

**Returns:**
- `bool`: True if the locale was removed, False if it didn't exist

#### get_custom_locales()

Get all custom locales defined for this keyboard.

**Returns:**
- `Dict[str, str]`: Dictionary of custom locale codes to display names

#### get_all_locales()

Get all available locales including built-in and custom ones.

**Returns:**
- `Dict[str, str]`: Combined dictionary of all available locales

#### to_json()

Convert keyboard to JSON string.

**Returns:**
- `str`: JSON representation of the keyboard

#### from_json(json_str)

Create keyboard instance from JSON string.

**Parameters:**
- `json_str` (str): JSON string representation of a keyboard

**Returns:**
- `InlineKeyboard`: Reconstructed keyboard instance

#### clear_pagination_hashes(source=None)

Clear stored pagination hashes for memory management.

**Parameters:**
- `source` (Optional[str]): Specific source to clear. If None, clears all hashes.

**Returns:**
- `int`: Number of hashes cleared

#### get_pagination_hash_stats()

Get statistics about stored pagination hashes.

**Returns:**
- `Dict[str, Any]`: Dictionary with hash storage statistics

### Properties

#### pyrogram_markup

Get the Pyrogram InlineKeyboardMarkup for this keyboard.

**Returns:**
- `InlineKeyboardMarkup`: Pyrogram-compatible markup

### Class Methods

#### clear_pagination_hashes(source=None)

Clear stored pagination hashes for memory management.

#### get_pagination_hash_stats()

Get statistics about stored pagination hashes.