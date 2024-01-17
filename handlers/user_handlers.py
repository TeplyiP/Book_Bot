from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
import database.database as DB
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData, IsCallBackInLibrary
from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                    create_edit_keyboard)
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book
from keyboards.library_kb import create_books_keyboard

router = Router()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if DB.check_id_in_base(message.from_user.id)==False:
        DB.add_user(message.from_user.id,message.from_user.full_name)


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


# Этот хэндлер будет срабатывать на команду "/beginning"
# и отправлять пользователю первую страницу книги с кнопками пагинации
@router.message(Command(commands='begining'))
async def process_beginning_command(message: Message):
    DB.reset_cur_page_to_1(message.from_user.id)
    curr_page=1
    curr_table=DB.get_table_name(message.from_user.id)
    text =DB.get_page_text(curr_page,curr_table)
    if text is not None:
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{curr_page}',
                'forward'
            )
        )
    else:
        await message.answer(
            text='Конец книги',
            reply_markup=create_pagination_keyboard(
                'backward'
            )
        )




# Этот хэндлер будет срабатывать на команду "/continue"
# и отправлять пользователю страницу книги, на которой пользователь
# остановился в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    curr_page=DB.get_current_page(message.from_user.id)
    curr_table=DB.get_table_name(message.from_user.id)
    text =DB.get_page_text(curr_page,curr_table)
    if text is not None:
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{curr_page}',
                'forward'
            )
        )
    else:
        await message.answer(
            text='Конец книги',
            reply_markup=create_pagination_keyboard(
                'backward'
            )
        )

# Этот хэндлер будет срабатывать на команду "/library"
# и отправлять пользователю список книг
@router.message(Command(commands='library'))
async def process_books_command(message: Message):
    book_list=DB.get_lib_dict()
    await message.answer(
        text='Вот список книг которые у нас есть',
        reply_markup=create_books_keyboard(
            book_list
        )
    )


# Этот хэндлер будет срабатывать на команду "/bookmarks"
# и отправлять пользователю список сохраненных закладок,
# если они есть или сообщение о том, что закладок нет
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if DB.users_db[message.from_user.id]["bookmarks"]:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *DB.users_db[message.from_user.id]["bookmarks"]
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    curr_page=DB.get_current_page(callback.from_user.id)
    curr_table=DB.get_table_name(callback.from_user.id)
    len_book=DB.get_total_pages(curr_table)
    if curr_page < len_book:
        DB.increment_current_page(callback.from_user.id)
        text = DB.get_page_text(curr_page+1,curr_table)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{curr_page+1}',
                'forward'
            )
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с сообщением-книгой
@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    curr_page=DB.get_current_page(callback.from_user.id)
    curr_table=DB.get_table_name(callback.from_user.id)
    len_book=DB.get_total_pages(curr_table)
    if curr_page > 1:
        DB.decrement_current_page(callback.from_user.id)
        text = DB.get_page_text(curr_page-1,curr_table)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{curr_page-1}',
                'forward'
            )
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(IsCallBackInLibrary())
async def process_page_press(callback: CallbackQuery):
    DB.set_user_book(callback.from_user.id,callback.data)
    #await callback.answer('Книга выбрана!')
    curr_page=DB.get_current_page(callback.from_user.id)
    curr_table=DB.get_table_name(callback.from_user.id)
    text =DB.get_page_text(curr_page,curr_table)
    if text is not None:
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{curr_page}',
                'forward'
            )
        )
    else:
        await callback.message.edit_text(
            text='Конец книги',
            reply_markup=create_pagination_keyboard(
                'backward'
            )
        )


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    DB.users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            'backward',
            f'{DB.users_db[callback.from_user.id]["page"]}/{len(book)}',
            'forward'
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "редактировать" под списком закладок
@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *DB.users_db[callback.from_user.id]["bookmarks"]
        )
    )
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# "отменить" во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    DB.users_db[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3])
    )
    if DB.users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_keyboard(
                *DB.users_db[callback.from_user.id]["bookmarks"]
            )
        )
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()