"""
PyKeyboard Sequential Examples for Telegram Bot Development

This file contains practical examples of how to use PyKeyboard in real Telegram bot scenarios.
Each example builds upon the previous one, showing progressive complexity.
"""

from pykeyboard import InlineButton, InlineKeyboard, ReplyButton, ReplyKeyboard


# Example 1: Basic Inline Keyboard for a Simple Menu
def create_main_menu():
    """Create a basic main menu with common bot actions."""
    keyboard = InlineKeyboard(row_width=2)

    keyboard.add(
        InlineButton("📊 Statistics", "menu:stats"),
        InlineButton("⚙️ Settings", "menu:settings"),
        InlineButton("ℹ️ Help", "menu:help"),
        InlineButton("📞 Support", "menu:support"),
    )

    return keyboard


# Example 2: Reply Keyboard for User Input
def create_contact_keyboard():
    """Create a reply keyboard for collecting user contact information."""
    keyboard = ReplyKeyboard(
        resize_keyboard=True,
        one_time_keyboard=True,
        placeholder="Choose an option...",
    )

    keyboard.row(
        ReplyButton("📱 Share Phone", request_contact=True),
        ReplyButton("📍 Share Location", request_location=True),
    )
    keyboard.row(ReplyButton("❌ Skip"))

    return keyboard


# Example 3: Dynamic Pagination for Product Catalog
def create_product_catalog_page(products, current_page, items_per_page=5):
    """Create a paginated product catalog."""
    keyboard = InlineKeyboard()

    # Calculate pagination
    total_pages = (len(products) + items_per_page - 1) // items_per_page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, len(products))

    # Add product buttons
    for i in range(start_idx, end_idx):
        product = products[i]
        keyboard.add(
            InlineButton(
                f"{product['name']} - ${product['price']}",
                f"product:{product['id']}",
            )
        )

    # Add pagination controls
    if total_pages > 1:
        keyboard.paginate(total_pages, current_page, "catalog:{number}")

    # Add navigation buttons
    keyboard.row(
        InlineButton("🏠 Main Menu", "menu:main"),
        InlineButton("🛒 Cart", "cart:view"),
    )

    return keyboard


# Example 4: Language Selection with Custom Locales
def create_language_selector():
    """Create a language selection keyboard with custom locales."""
    keyboard = InlineKeyboard(row_width=2)

    # Add built-in languages
    keyboard.languages("lang:{locale}", ["en_US", "es_ES", "fr_FR", "de_DE"], 2)

    # Add custom locales
    keyboard.add_custom_locale("pt_BR", "🇧🇷 Português")
    keyboard.add_custom_locale("ru_RU", "🇷🇺 Русский")

    # Add custom language buttons
    keyboard.row(
        InlineButton("🇧🇷 Português", "lang:pt_BR"),
        InlineButton("🇷🇺 Русский", "lang:ru_RU"),
    )

    return keyboard


# Example 5: Advanced Settings Menu with Conditional Buttons
def create_settings_menu(user_premium=False, notifications_enabled=True):
    """Create a settings menu with conditional options."""
    keyboard = InlineKeyboard(row_width=2)

    # Always available settings
    keyboard.add(
        InlineButton("🔔 Notifications", "settings:notifications"),
        InlineButton("🌐 Language", "settings:language"),
        InlineButton("🎨 Theme", "settings:theme"),
    )

    # Premium-only features
    if user_premium:
        keyboard.add(
            InlineButton("⭐ Premium Features", "settings:premium"),
            InlineButton("📊 Advanced Stats", "settings:advanced_stats"),
        )

    # Notification-specific settings
    if notifications_enabled:
        keyboard.row(
            InlineButton("🔕 Mute All", "settings:mute_all"),
            InlineButton("⏰ Schedule", "settings:notification_schedule"),
        )

    # Always at the bottom
    keyboard.row(InlineButton("⬅️ Back to Menu", "menu:main"))

    return keyboard


# Example 6: Interactive Quiz with Answer Validation
def create_quiz_question(question_data, selected_answer=None):
    """Create a quiz question with answer options."""
    keyboard = InlineKeyboard(row_width=2)

    for i, option in enumerate(question_data["options"]):
        # Mark selected answer
        text = f"{'✅ ' if selected_answer == i else ''}{option}"
        callback_data = f"quiz:answer:{question_data['id']}:{i}"
        keyboard.add(InlineButton(text, callback_data))

    # Add navigation
    keyboard.row(
        InlineButton("⬅️ Previous", f"quiz:prev:{question_data['id']}"),
        InlineButton("➡️ Next", f"quiz:next:{question_data['id']}"),
    )

    return keyboard


# Example 7: File Management Interface
def create_file_browser(files, current_path="/", page=1):
    """Create a file browser interface."""
    keyboard = InlineKeyboard(row_width=3)

    # Add file/folder buttons
    for file_info in files:
        icon = "📁" if file_info["is_dir"] else "📄"
        text = f"{icon} {file_info['name']}"
        callback_data = f"file:{'dir' if file_info['is_dir'] else 'file'}:{file_info['path']}"
        keyboard.add(InlineButton(text, callback_data))

    # Add navigation
    if page > 1:
        keyboard.row(
            InlineButton("⬅️ Previous", f"files:{current_path}:{page-1}")
        )

    keyboard.row(
        InlineButton("📤 Upload", "file:upload"),
        InlineButton("🆕 New Folder", "file:new_folder"),
        InlineButton("⬆️ Up", f"file:up:{current_path}"),
    )

    return keyboard


# Example 8: E-commerce Cart Management
def create_cart_management(cart_items, total_price):
    """Create cart management interface."""
    keyboard = InlineKeyboard(row_width=2)

    # Add cart items
    for item in cart_items:
        text = f"{item['name']} x{item['quantity']} - ${item['price'] * item['quantity']}"
        keyboard.add(InlineButton(text, f"cart:edit:{item['id']}"))

    # Add summary and actions
    keyboard.row(InlineButton(f"💰 Total: ${total_price}", "cart:total"))
    keyboard.row(
        InlineButton("✅ Checkout", "cart:checkout"),
        InlineButton("🗑️ Clear Cart", "cart:clear"),
    )
    keyboard.row(InlineButton("⬅️ Continue Shopping", "shop:continue"))

    return keyboard


# Example 9: Admin Panel with Role-based Access
def create_admin_panel(user_role="user"):
    """Create admin panel with role-based access control."""
    keyboard = InlineKeyboard(row_width=2)

    # Basic admin functions
    keyboard.add(
        InlineButton("👥 User Management", "admin:users"),
        InlineButton("📊 Analytics", "admin:analytics"),
    )

    # Advanced functions for super admins
    if user_role == "super_admin":
        keyboard.add(
            InlineButton("⚙️ System Settings", "admin:system"),
            InlineButton("🛡️ Security", "admin:security"),
            InlineButton("💾 Backup", "admin:backup"),
            InlineButton("🔄 Maintenance", "admin:maintenance"),
        )

    # Moderation tools for moderators and above
    if user_role in ["moderator", "admin", "super_admin"]:
        keyboard.row(
            InlineButton("🚫 Ban User", "admin:ban"),
            InlineButton("⚠️ Warn User", "admin:warn"),
        )

    keyboard.row(InlineButton("⬅️ Back to Menu", "menu:main"))

    return keyboard


# Example 10: Complete Bot Workflow Integration
def handle_callback_query(callback_query):
    """Example of how to handle callback queries in a bot."""
    data = callback_query.data

    if data.startswith("menu:"):
        action = data.split(":")[1]
        if action == "stats":
            return create_stats_keyboard()
        elif action == "settings":
            return create_settings_menu()
        # ... handle other menu actions

    elif data.startswith("product:"):
        product_id = data.split(":")[1]
        return create_product_detail_keyboard(product_id)

    elif data.startswith("cart:"):
        action = data.split(":")[1]
        if action == "add":
            # Add to cart logic
            return create_cart_confirmation_keyboard()
        # ... handle other cart actions

    # Default fallback
    return create_main_menu()


# Helper functions for the complete workflow
def create_stats_keyboard():
    """Create statistics display keyboard."""
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("📈 Daily Stats", "stats:daily"),
        InlineButton("📊 Weekly Stats", "stats:weekly"),
        InlineButton("📅 Monthly Stats", "stats:monthly"),
    )
    keyboard.row(InlineButton("⬅️ Back", "menu:main"))
    return keyboard


def create_product_detail_keyboard(product_id):
    """Create product detail view keyboard."""
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        InlineButton("🛒 Add to Cart", f"cart:add:{product_id}"),
        InlineButton("❤️ Add to Wishlist", f"wishlist:add:{product_id}"),
        InlineButton("⭐ Rate Product", f"rating:show:{product_id}"),
        InlineButton("📝 Reviews", f"reviews:show:{product_id}"),
    )
    keyboard.row(InlineButton("⬅️ Back to Catalog", "catalog:1"))
    return keyboard


def create_cart_confirmation_keyboard():
    """Create cart addition confirmation keyboard."""
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("✅ Continue Shopping", "shop:continue"),
        InlineButton("🛒 View Cart", "cart:view"),
    )
    return keyboard


# Usage examples
if __name__ == "__main__":
    # Example usage of the keyboards
    print("=== PyKeyboard Sequential Examples ===\n")

    # 1. Main Menu
    print("1. Main Menu:")
    main_menu = create_main_menu()
    print(f"   Keyboard has {len(main_menu.keyboard)} rows")
    print(f"   Total buttons: {sum(len(row) for row in main_menu.keyboard)}\n")

    # 2. Contact Keyboard
    print("2. Contact Keyboard:")
    contact_kb = create_contact_keyboard()
    print(f"   Reply keyboard with placeholder: {contact_kb.placeholder}\n")

    # 3. Product Catalog
    print("3. Product Catalog:")
    sample_products = [
        {"id": 1, "name": "Laptop", "price": 999},
        {"id": 2, "name": "Mouse", "price": 25},
        {"id": 3, "name": "Keyboard", "price": 75},
    ]
    catalog = create_product_catalog_page(sample_products, 1)
    print(f"   Catalog page with {len(catalog.keyboard)} rows\n")

    # 4. Language Selector
    print("4. Language Selector:")
    lang_kb = create_language_selector()
    print(f"   Language selection with {len(lang_kb.keyboard)} rows\n")

    # 5. Settings Menu
    print("5. Settings Menu (Premium User):")
    settings = create_settings_menu(user_premium=True)
    print(f"   Premium settings with {len(settings.keyboard)} rows\n")

    print("All examples created successfully!")
    print("These keyboards can be used with:")
    print("await message.reply_text('Choose an option:', reply_markup=keyboard)")
