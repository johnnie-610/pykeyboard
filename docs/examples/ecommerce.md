# E-commerce Bot Example

This example demonstrates how to create an e-commerce bot with product catalog, shopping cart, and checkout functionality using PyKeyboard.

<strong><em>Note: ALTHOUGH WE BELIEVE THIS EXAMPLE SHOULD WORK, IT IS NOT TESTED AND MIGHT NOT WORK. </em></strong>
<strong><em>USE AT YOUR OWN RISK. YOU CAN INSTEAD REFER TO THIS SCRIPT WHICH HAS BEEN TESTED AND WORKS: <a href="https://github.com/johnnie-610/pykeyboard/blob/main/showcase_bot.py">Showcase Bot</a>.</em></strong>

## Overview

This example shows:
- Product catalog with pagination
- Shopping cart management
- Checkout process
- Order confirmation
- Using KeyboardFactory for common patterns

## Code Example

```python
from pyrogram import Client, filters
from pykeyboard import KeyboardFactory, InlineKeyboard, InlineButton
from typing import Dict, List
import json

app = Client("ecommerce_bot")

# Mock product data
PRODUCTS = [
    {"id": 1, "name": "Wireless Headphones", "price": 99.99, "category": "Electronics"},
    {"id": 2, "name": "Smart Watch", "price": 199.99, "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 79.99, "category": "Appliances"},
    {"id": 4, "name": "Running Shoes", "price": 129.99, "category": "Sports"},
    {"id": 5, "name": "Yoga Mat", "price": 39.99, "category": "Sports"},
    {"id": 6, "name": "Cookbook", "price": 24.99, "category": "Books"},
]

# User cart storage (in production, use a database)
user_carts: Dict[int, List[Dict]] = {}

def get_products_page(page: int, per_page: int = 3):
    """Get products for a specific page."""
    start = (page - 1) * per_page
    end = start + per_page
    return PRODUCTS[start:end]

def create_product_keyboard(products: List[Dict], current_page: int, total_pages: int):
    """Create keyboard for product listing with pagination."""
    keyboard = InlineKeyboard()

    # Add products
    for product in products:
        keyboard.row(
            InlineButton(
                f"{product['name']} - ${product['price']}",
                callback_data=f"product:{product['id']}"
            ),
            InlineButton("🛒 Add to Cart", callback_data=f"add_cart:{product['id']}")
        )

    # Add pagination
    if total_pages > 1:
        keyboard.paginate(total_pages, current_page, "page:{number}")

    # Add cart and navigation
    keyboard.row(
        InlineButton("🛒 View Cart", callback_data="view_cart"),
        InlineButton("📂 Categories", callback_data="categories")
    )

    return keyboard

def create_cart_keyboard(cart_items: List[Dict]):
    """Create keyboard for cart management."""
    keyboard = InlineKeyboard()

    if not cart_items:
        keyboard.add(InlineButton("🛍️ Continue Shopping", callback_data="page:1"))
        return keyboard

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # Cart items
    for item in cart_items:
        keyboard.row(
            InlineButton(
                f"{item['name']} x{item['quantity']} - ${item['price'] * item['quantity']:.2f}",
                callback_data=f"cart_item:{item['id']}"
            ),
            InlineButton("➕", callback_data=f"cart_add:{item['id']}"),
            InlineButton("➖", callback_data=f"cart_remove:{item['id']}")
        )

    # Total and actions
    keyboard.row(InlineButton(f"💰 Total: ${total:.2f}", callback_data="total"))
    keyboard.row(
        InlineButton("✅ Checkout", callback_data="checkout"),
        InlineButton("🛍️ Continue Shopping", callback_data="page:1"),
        InlineButton("🗑️ Clear Cart", callback_data="clear_cart")
    )

    return keyboard

@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    user_carts[user_id] = []

    products = get_products_page(1)
    keyboard = create_product_keyboard(products, 1, (len(PRODUCTS) + 2) // 3)

    await message.reply_text(
        "🛍️ **Welcome to our Store!**\n\n"
        "Browse our products and add them to your cart:",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex(r"^page:"))
async def handle_pagination(client, callback_query):
    page = int(callback_query.data.split(":")[1])
    products = get_products_page(page)
    total_pages = (len(PRODUCTS) + 2) // 3
    keyboard = create_product_keyboard(products, page, total_pages)

    await callback_query.edit_message_text(
        f"🛍️ **Products (Page {page}/{total_pages})**\n\n"
        "Browse our products:",
        reply_markup=keyboard
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^add_cart:"))
async def handle_add_to_cart(client, callback_query):
    user_id = callback_query.from_user.id
    product_id = int(callback_query.data.split(":")[1])

    if user_id not in user_carts:
        user_carts[user_id] = []

    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        # Check if product already in cart
        cart_item = next((item for item in user_carts[user_id] if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += 1
        else:
            user_carts[user_id].append({**product, 'quantity': 1})

        await callback_query.answer(f"✅ {product['name']} added to cart!")

@app.on_callback_query(filters.regex(r"^view_cart$"))
async def handle_view_cart(client, callback_query):
    user_id = callback_query.from_user.id
    cart_items = user_carts.get(user_id, [])
    keyboard = create_cart_keyboard(cart_items)

    cart_text = "🛒 **Your Cart**\n\n"
    if not cart_items:
        cart_text += "Your cart is empty."
    else:
        for item in cart_items:
            cart_text += f"• {item['name']} x{item['quantity']} - ${item['price'] * item['quantity']:.2f}\n"
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        cart_text += f"\n**Total: ${total:.2f}**"

    await callback_query.edit_message_text(cart_text, reply_markup=keyboard)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^checkout$"))
async def handle_checkout(client, callback_query):
    user_id = callback_query.from_user.id
    cart_items = user_carts.get(user_id, [])

    if not cart_items:
        await callback_query.answer("Your cart is empty!")
        return

    total = sum(item['price'] * item['quantity'] for item in cart_items)

    # Create confirmation keyboard
    keyboard = KeyboardFactory.create_confirmation_keyboard(
        yes_text="✅ Confirm Order",
        no_text="❌ Cancel",
        callback_pattern="order_{action}"
    )

    order_summary = "📋 **Order Summary**\n\n"
    for item in cart_items:
        order_summary += f"• {item['name']} x{item['quantity']} - ${item['price'] * item['quantity']:.2f}\n"
    order_summary += f"\n**Total: ${total:.2f}**\n\nConfirm your order?"

    await callback_query.edit_message_text(order_summary, reply_markup=keyboard)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^order_"))
async def handle_order_confirmation(client, callback_query):
    action = callback_query.data.split("_")[1]
    user_id = callback_query.from_user.id

    if action == "yes":
        # Process order (in production, save to database)
        cart_items = user_carts.get(user_id, [])
        total = sum(item['price'] * item['quantity'] for item in cart_items)

        # Clear cart
        user_carts[user_id] = []

        await callback_query.edit_message_text(
            "✅ **Order Confirmed!**\n\n"
            f"Thank you for your purchase!\n"
            f"Total: ${total:.2f}\n\n"
            "You will receive a confirmation email shortly.",
            reply_markup=InlineKeyboard().add(
                InlineButton("🛍️ Continue Shopping", callback_data="page:1")
            )
        )
    else:
        await callback_query.edit_message_text(
            "❌ Order cancelled.\n\n"
            "You can continue shopping:",
            reply_markup=create_product_keyboard(get_products_page(1), 1, (len(PRODUCTS) + 2) // 3)
        )

    await callback_query.answer()

if __name__ == "__main__":
    app.run()
```

## Features Demonstrated

- Product catalog with pagination
- Shopping cart management
- Add/remove items from cart
- Checkout process
- Order confirmation
- Using KeyboardFactory for common UI patterns

## E-commerce Flow

```
Browse Products → Add to Cart → View Cart → Checkout → Order Confirmation
```

## Running the Example

1. Install PyKeyboard: `pip install pykeyboard-kurigram`
2. Set up your bot token
3. Run the script: `python ecommerce_bot.py`
4. Send `/start` to begin shopping
5. Browse products, add to cart, and checkout