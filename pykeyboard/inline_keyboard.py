# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# This file is part of the pykeyboard-kurigram library
# 
# pykeyboard/inline_keyboard.py

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dataclasses import dataclass
from .keyboard_base import KeyboardBase, InlineButton
from functools import lru_cache


@dataclass
class InlineKeyboard(InlineKeyboardMarkup, KeyboardBase):
    _PAGINATION_SYMBOLS = {
        "first": "« {}",
        "prev": "‹ {}",
        "current": "· {} ·",
        "next": "{} ›",
        "last": "{} »",
    }

    @staticmethod
    def _get_locales() -> dict[str, str]:
        return {
            "be_BY": f"🇧🇾 Беларуская",  # Belarusian - Belarus
            "de_DE": f"🇩🇪 Deutsch",  # German - Germany
            "zh_CN": f"🇨🇳 中文",  # Chinese - China
            "en_US": f"🇬🇧  English",  # English - United Kingdom
            "fr_FR": f"🇫🇷 Français",  # French - France
            "id_ID": f"🇮🇩 Bahasa Indonesia",  # Indonesian - Indonesia
            "it_IT": f"🇮🇹 Italiano",  # Italian - Italy
            "ko_KR": f"🇰🇷 한국어",  # Korean - Korea
            "tr_TR": f"🇹🇷 Türkçe",  # Turkish - Turkey
            "ru_RU": f"🇷🇺 Русский",  # Russian - Russia
            "es_ES": f"🇪🇸 Español",  # Spanish - Spain
            "uk_UA": f"🇺🇦 Українська",  # Ukrainian - Ukraine
            "uz_UZ": f"🇺🇿 Oʻzbekcha",  # Uzbek - Uzbekistan
        }

    def __post_init__(self):
        super().__init__(inline_keyboard=self.keyboard) # type: ignore
        self.callback_pattern = ""
        self.count_pages = 0
        self.current_page = 0

    @staticmethod
    @lru_cache(maxsize=128)
    def _create_button(text: str, callback_data: str) -> InlineKeyboardButton:
        """Create cached button with optimized parameters."""
        return InlineButton(text=text, callback_data=callback_data)

    def paginate(
        self, count_pages: int, current_page: int, callback_pattern: str
    ) -> None:
        """Optimized pagination with better edge case handling.

        Args:
            count_pages (int): Total number of pages.
            current_page (int): The page number currently being viewed.
            callback_pattern (str): The pattern used for callback data.

        Example:
            >>> keyboard = InlineKeyboard()
            >>> keyboard.paginate(10, 1, 'page_{number}')
            >>> print(keyboard.keyboard)
            [[InlineKeyboardButton(text='· 1 ·', callback_data='page_1'), ...]]

        """
        self.count_pages = max(1, count_pages)
        self.current_page = max(1, min(current_page, self.count_pages))
        self.callback_pattern = callback_pattern

        if self.count_pages <= 5:
            pagination = self._build_small_pagination()
        else:
            pagination = self._build_large_pagination()

        self.keyboard.append(pagination) # type: ignore

    def _build_small_pagination(self) -> list[InlineKeyboardButton]:
        return [
            self._create_button(
                text=(
                    self._PAGINATION_SYMBOLS["current"].format(i)
                    if i == self.current_page
                    else str(i)
                ),
                callback_data=self.callback_pattern.format(number=i),
            )
            for i in range(1, self.count_pages + 1)
        ]

    def _build_large_pagination(self) -> list[InlineKeyboardButton]:
        if self.current_page <= 3:
            return self._build_left_pagination()
        elif self.current_page > self.count_pages - 3:
            return self._build_right_pagination()
        return self._build_middle_pagination()

    def _build_left_pagination(self) -> list[InlineKeyboardButton]:
        buttons = []
        for i in range(1, 6):
            if i == self.current_page:
                text = self._PAGINATION_SYMBOLS["current"].format(i)
            elif i == 4:
                text = self._PAGINATION_SYMBOLS["next"].format(i)
            elif i == 5:
                text = self._PAGINATION_SYMBOLS["last"].format(self.count_pages)
                i = self.count_pages
            else:
                text = str(i)
            buttons.append( # type: ignore
                self._create_button(
                    text=text, callback_data=self.callback_pattern.format(number=i)
                )
            )
        return buttons # type: ignore

    def _build_middle_pagination(self) -> list[InlineKeyboardButton]:
        return [
            self._create_button(
                text=self._PAGINATION_SYMBOLS["first"].format(1),
                callback_data=self.callback_pattern.format(number=1),
            ),
            self._create_button(
                text=self._PAGINATION_SYMBOLS["prev"].format(self.current_page - 1),
                callback_data=self.callback_pattern.format(
                    number=self.current_page - 1
                ),
            ),
            self._create_button(
                text=self._PAGINATION_SYMBOLS["current"].format(self.current_page),
                callback_data=self.callback_pattern.format(number=self.current_page),
            ),
            self._create_button(
                text=self._PAGINATION_SYMBOLS["next"].format(self.current_page + 1),
                callback_data=self.callback_pattern.format(
                    number=self.current_page + 1
                ),
            ),
            self._create_button(
                text=self._PAGINATION_SYMBOLS["last"].format(self.count_pages),
                callback_data=self.callback_pattern.format(number=self.count_pages),
            ),
        ]

    def _build_right_pagination(self) -> list[InlineKeyboardButton]:
        buttons = [
            self._create_button(
                text=self._PAGINATION_SYMBOLS["first"].format(1),
                callback_data=self.callback_pattern.format(number=1),
            ),
            self._create_button(
                text=self._PAGINATION_SYMBOLS["prev"].format(self.count_pages - 3),
                callback_data=self.callback_pattern.format(number=self.count_pages - 3),
            ),
        ]

        for i in range(self.count_pages - 2, self.count_pages + 1):
            text = (
                self._PAGINATION_SYMBOLS["current"].format(i)
                if i == self.current_page
                else str(i)
            )
            buttons.append(
                self._create_button(
                    text=text, callback_data=self.callback_pattern.format(number=i)
                )
            )
        return buttons

    def languages(
        self, callback_pattern: str, locales: str | list[str], row_width: int = 2
    ) -> None:
        """Optimized language selection keyboard."""
        if isinstance(locales, str):
            locales = [locales]

        buttons = [
            self._create_button(
                text=self._get_locales().get(locale, "Invalid locale"),
                callback_data=callback_pattern.format(locale=locale),
            )
            for locale in locales
            if locale in self._get_locales()
        ]

        self.keyboard = [
            buttons[i : i + row_width] for i in range(0, len(buttons), row_width)
        ]
