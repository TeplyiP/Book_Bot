from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_books_keyboard(args: list) -> InlineKeyboardMarkup:
    # Создаем объект клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Наполняем клавиатуру кнопками-книгами
    for button in args:
        kb_builder.row(InlineKeyboardButton(
            text=button[0],
            callback_data=button[1]
        ))
    return kb_builder.as_markup()