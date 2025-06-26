# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# This file is part of the pykeyboard-kurigram library
# 
# pykeyboard/keyboard_base.py

from dataclasses import dataclass, field
from pyrogram.types import InlineKeyboardButton, WebAppInfo, CallbackGame, LoginUrl


@dataclass
class KeyboardBase:
    row_width: int = 3
    keyboard: list[list] = field(default_factory=list)

    def add(self, *args: object) -> None:
        self.keyboard = [
            list(args[i : i + self.row_width])
            for i in range(0, len(args), self.row_width)
        ]
        # Update the underlying Pyrogram structure
        self._update_keyboard()

    def row(self, *args: object) -> None:
        self.keyboard.append(list(args))
        # Update the underlying Pyrogram structure  
        self._update_keyboard()
    
    def _update_keyboard(self):
        """Override in subclasses to update the underlying Pyrogram structure"""
        pass


@dataclass
class Button:
    text: str

    def __post_init__(self):
        if not isinstance(self.text, str):
            raise ValueError("Button text must be a string")


@dataclass
class InlineButton(Button, InlineKeyboardButton):
    callback_data: str | bytes | None = None
    url: str | None = None
    web_app: WebAppInfo | None = None
    login_url: LoginUrl | None = None
    user_id: int | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None
    callback_game: CallbackGame | None = None
    requires_password: bool | None = None
    pay: bool | None = None
    copy_text: str | None = None

    def __post_init__(self):
        Button.__post_init__(self)
        InlineKeyboardButton.__init__(
            self,
            text=self.text,
            callback_data=self.callback_data,
            url=self.url,
            web_app=self.web_app,
            login_url=self.login_url,
            user_id=self.user_id,
            switch_inline_query=self.switch_inline_query,
            switch_inline_query_current_chat=self.switch_inline_query_current_chat,
            callback_game=self.callback_game,
            requires_password=self.requires_password,
            pay=self.pay,
            copy_text=self.copy_text,
        )