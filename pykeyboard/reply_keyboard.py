# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# This file is part of the pykeyboard-kurigram library

from dataclasses import dataclass
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove, # type: ignore
    ForceReply,
    KeyboardButtonPollType,
    KeyboardButtonRequestUsers,
    KeyboardButtonRequestChat,
    WebAppInfo,
)
from .keyboard_base import KeyboardBase, Button


@dataclass
class ReplyKeyboard(ReplyKeyboardMarkup, KeyboardBase):
    is_persistent: bool | None = None
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    selective: bool | None = None
    placeholder: str | None = None

    def __post_init__(self):
        super().__init__(
            keyboard=self.keyboard, # type: ignore
            is_persistent=self.is_persistent, # type: ignore
            resize_keyboard=self.resize_keyboard, # type: ignore
            one_time_keyboard=self.one_time_keyboard, # type: ignore
            selective=self.selective, # type: ignore
            placeholder=self.placeholder, # type: ignore
        )


@dataclass
class ReplyButton(KeyboardButton, Button):
    request_contact: bool | None = None
    request_location: bool | None = None
    request_poll: KeyboardButtonPollType | None = None
    request_users: KeyboardButtonRequestUsers | None = None
    request_chat: KeyboardButtonRequestChat | None = None
    web_app: WebAppInfo | None = None

    def __post_init__(self):
        super().__post_init__()
        super(KeyboardButton, self).__init__(
            text=self.text, # type: ignore
            request_contact=self.request_contact, # type: ignore
            request_location=self.request_location, # type: ignore
            request_poll=self.request_poll, # type: ignore
            request_users = self.request_users, # type: ignore
            request_chat = self.request_chat, # type: ignore
            web_app=self.web_app, # type: ignore
        )


@dataclass
class PyReplyKeyboardRemove(ReplyKeyboardRemove):
    selective: bool | None = None

    def __post_init__(self):
        super().__init__(selective=self.selective) # type: ignore


@dataclass
class PyForceReply(ForceReply):
    selective: bool | None = None
    placeholder: str | None = None

    def __post_init__(self):
        super().__init__(selective=self.selective, placeholder=self.placeholder) # type: ignore
