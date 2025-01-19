# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ForceReply,
    RequestChannelInfo,
    RequestChatInfo,
    RequestUserInfo,
    RequestPollInfo,
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
            keyboard=self.keyboard,
            is_persistent=self.is_persistent,
            resize_keyboard=self.resize_keyboard,
            one_time_keyboard=self.one_time_keyboard,
            selective=self.selective,
            placeholder=self.placeholder,
        )


@dataclass
class ReplyButton(KeyboardButton, Button):
    request_contact: bool | None = None
    request_location: bool | None = None
    request_poll: RequestPollInfo | None = None
    request_peer: RequestUserInfo | RequestChannelInfo | RequestChatInfo | None = None
    web_app: WebAppInfo | None = None

    def __post_init__(self):
        super().__post_init__()
        super(KeyboardButton, self).__init__(
            text=self.text,
            request_contact=self.request_contact,
            request_location=self.request_location,
            request_poll=self.request_poll,
            request_peer=self.request_peer,
            web_app=self.web_app,
        )


@dataclass
class ReplyKeyboardRemove(ReplyKeyboardRemove):
    selective: bool | None = None

    def __post_init__(self):
        super().__init__(selective=self.selective)


@dataclass
class ForceReply(ForceReply):
    selective: bool | None = None
    placeholder: str | None = None

    def __post_init__(self):
        super().__init__(selective=self.selective, placeholder=self.placeholder)
