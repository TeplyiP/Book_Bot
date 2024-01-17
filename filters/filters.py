from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from database.database import get_tabel_names_for_handler


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('del') and callback.data[:-3].isdigit()
    
#фильтр на колбэк с названием таблицы. проверяет
    #есть ли в библиотеке таблица совпадающая с колбэком
class IsCallBackInLibrary(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        names=get_tabel_names_for_handler()
        if callback.data in names:
            return True
        else:
            return False