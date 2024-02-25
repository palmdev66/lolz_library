from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils import db as api

async def start() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="📕 Все книги", callback_data="books_all")
        )
    
    kb.row(
        InlineKeyboardButton(text="🔎 Поиск", callback_data="books_find")
        )
    
    kb.row(
        InlineKeyboardButton(text="➕ Добавить книгу", callback_data="books_add")
        )

    return kb.as_markup(resize_keyboard=True)

async def books(filter=None, key=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if not filter:
        books = await api.get_books()
    if filter == "keyword":
        books = await api.find_books_keyword(key)
    if filter == "genre":
        books = await api.find_books_genre(key)

    for book in books:
        author = book[2]
        title = book[1]
        id = book[0]

        kb.row(
            InlineKeyboardButton(text=f"{title} ({author})", callback_data=f"book_{id}")
            )
    
    kb.row(
        InlineKeyboardButton(text="⬅️ В меню", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)

async def genres(filter=None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if not filter:
        call_data = "genre_"
            
    if filter == "add":
        call_data = "add_genre_"

    genres = await api.get_genres()
    for genre in genres:
        name = genre[1]
        id = genre[0]
        kb.row(
            InlineKeyboardButton(text=name, callback_data=f"{call_data}{name}")
            )

    kb.adjust(2)

    kb.row(
        InlineKeyboardButton(text="⬅️ В меню", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)

async def find() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.row(
        InlineKeyboardButton(text="✨ По жанрам", callback_data="find_genre")
        )
    
    kb.row(
        InlineKeyboardButton(text="🗣️ По ключевому слову", callback_data="find_keyword")
        )
    
    kb.row(
        InlineKeyboardButton(text="⬅️ В меню", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)

async def back() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.row(
        InlineKeyboardButton(text="⬅️ В меню", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)

async def confirm() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.row(
        InlineKeyboardButton(text="✅ Подтвердить", callback_data="add_confirm"),
        InlineKeyboardButton(text="❌ Отменить", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)

async def delete(book_id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.row(
        InlineKeyboardButton(text="🗑️ Удалить книгу", callback_data=f"delete_{book_id}")
        )

    kb.row(
        InlineKeyboardButton(text="⬅️ В меню", callback_data="start")
        )

    return kb.as_markup(resize_keyboard=True)