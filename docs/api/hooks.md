# Hooks & Validation

## ButtonValidator <span class="api-badge class">Class</span>

Configurable button validator with built-in and custom rules.

### Constructor

```python
ButtonValidator(include_defaults: bool = True)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_defaults` | `bool` | `True` | Include default validation rules (text length, callback data checks) |

---

### add_rule <span class="api-badge method">method</span>

Add a custom validation rule.

| Parameter | Type | Description |
|-----------|------|-------------|
| `rule` | `Callable[[Any], str \| None]` | Returns `None` if valid, error message if invalid |

**Returns:** `ButtonValidator` (chainable)

??? example "Usage"
    ```python
    from pykeyboard import ButtonValidator

    validator = ButtonValidator()
    validator.add_rule(lambda btn: "Too long" if len(btn.text) > 50 else None)
    ```

---

### validate_button <span class="api-badge method">method</span>

Validate a single button against all registered rules.

**Returns:** `dict[str, Any]`

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | `bool` | Whether the button passed all rules |
| `errors` | `list[str]` | Error messages from failed rules |
| `checked_rules` | `int` | Number of rules checked |

??? example "Usage"
    ```python
    from pykeyboard import ButtonValidator, InlineButton

    validator = ButtonValidator()
    result = validator.validate_button(InlineButton("OK", "ok"))
    print(result["is_valid"])       # True
    print(result["checked_rules"])  # number of default rules
    ```

---

## KeyboardHookManager <span class="api-badge class">Class</span>

Manages hooks for keyboard construction lifecycle.

### Hook Types

| Method | Hook Signature | When it Runs |
|--------|---------------|--------------|
| `add_button_hook(hook)` | `(button) → button` | Each button during construction |
| `add_pre_hook(hook)` | `(keyboard) → None` | Before construction |
| `add_post_hook(hook)` | `(keyboard) → None` | After construction |
| `add_error_hook(hook)` | `(exception, keyboard) → None` | When a hook raises |

All methods return `KeyboardHookManager` for chaining.

---

### process_button <span class="api-badge method">method</span>

Process a button through all button hooks.

```python
manager.process_button(button) -> Any
```

---

### execute_pre_hooks / execute_post_hooks <span class="api-badge method">method</span>

Execute all pre/post-construction hooks.

```python
manager.execute_pre_hooks(keyboard)
manager.execute_post_hooks(keyboard)
```

??? example "Full Example"
    ```python
    from pykeyboard import KeyboardHookManager

    manager = KeyboardHookManager()

    # Uppercase all button text
    manager.add_button_hook(
        lambda btn: setattr(btn, "text", btn.text.upper()) or btn
    )

    # Log keyboard construction
    manager.add_post_hook(
        lambda kb: print(f"Built keyboard with {len(kb.keyboard)} rows")
    )
    ```

---

## Convenience Functions

### validate_button <span class="api-badge method">function</span>

Quick-validate a button with default rules.

```python
from pykeyboard import validate_button, InlineButton

is_valid = validate_button(InlineButton("OK", "ok"))  # True
```

---

### validate_keyboard <span class="api-badge method">function</span>

Validate all buttons in a keyboard.

```python
from pykeyboard.hooks import validate_keyboard

result = validate_keyboard(kb)
```

**Returns:** `dict[str, Any]`

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | `bool` | All buttons valid |
| `total_buttons` | `int` | Total buttons checked |
| `valid_buttons` | `int` | Buttons that passed |
| `invalid_buttons` | `int` | Buttons that failed |
| `errors` | `list` | Detailed error info |
