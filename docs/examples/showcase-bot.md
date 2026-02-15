# Showcase Bot

The **showcase bot** is a fully tested, interactive Telegram bot that demonstrates every PyKeyboard feature in one place.

!!! tip "Recommended Reference"
Unlike the other example bots in this section, the showcase bot is **tested and maintained** as part of the repository. It is the canonical reference implementation.

## What it Covers

| Section        | Feature                                                 |
| -------------- | ------------------------------------------------------- |
| 🎯 Inline      | Action buttons, URL buttons, reactions                  |
| 📱 Reply       | Contact/location requests, remove keyboard, force reply |
| 📄 Pagination  | 3, 5, 10, 25, and 100-page demos with navigation        |
| 🌍 Languages   | Built-in + custom locales with `add_custom_locale`      |
| 🚨 Errors      | All 5 error types triggered and inspected live          |
| 🏗️ Builder     | Factory presets, fluent builder, hooks & validation     |
| 📊 Performance | Micro-benchmarks for keyboard creation                  |

Every section includes a **code-to-reproduce snippet** directly in the Telegram message.

## Running the Bot

```bash
export TELEGRAM_BOT_TOKEN="your_token"
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
python showcase_bot.py
```

Then send `/start` to the bot in Telegram.

## Source Code

- [showcase_bot.py on GitHub](https://github.com/johnnie-610/pykeyboard/blob/main/showcase_bot.py)
