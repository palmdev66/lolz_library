from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from utils import book
from keyboards import inline
from utils import db as api

router = Router()

class States(StatesGroup):
    book_info = State()
    keyword = State()
    title = State()
    author = State()
    desc = State()
    genre = State()
    preview = State()

# Хандлер на команду /start
async def start(msg: Message, state: FSMContext):
    await state.clear()

    keyboard = await inline.start()
    text = await book.start(msg.from_user.full_name)
    await msg.answer(text, reply_markup=keyboard)

# Тот же хандлер start, но сделанный под коллбек от кнопки назад
async def call_start(call: CallbackQuery, state: FSMContext):
    await state.clear()

    keyboard = await inline.start()
    text = await book.start(call.from_user.full_name)
    await call.message.edit_text(text, reply_markup=keyboard)

# Вывод списка всех книг
async def books_all(call: CallbackQuery):
    keyboard = await inline.books()
    text = await book.books()
    await call.message.edit_text(text, reply_markup=keyboard)

# Вывод подробностей о книге
async def book_info(call: CallbackQuery):
    book_id = call.data.split("_")[1]
    keyboard = await inline.delete(book_id)
    text = await book.info(book_id)
    await call.message.edit_text(text, reply_markup=keyboard)

# Вывод подробностей о книге
async def book_delete(call: CallbackQuery):
    book_id = call.data.split("_")[1]
    keyboard = await inline.back()
    await api.remove_book(book_id)
    await call.message.edit_text("✅ Книга успешно удалена!", reply_markup=keyboard)

# Меню выбора метода поиска
async def books_find(call: CallbackQuery):
    keyboard = await inline.find()
    text = await book.find("select")
    await call.message.edit_text(text, reply_markup=keyboard)

# Поиск по жанру
async def find_genre(call: CallbackQuery):
    keyboard = await inline.genres()
    text = await book.find("genre")
    await call.message.edit_text(text, reply_markup=keyboard)

# Результаты поиска по жанру
async def genre_results(call: CallbackQuery):
    print(call.data)
    id = call.data.split("_")[1]
    keyboard = await inline.books("genre", id)
    text = await book.books("genre", id)
    await call.message.edit_text(text, reply_markup=keyboard)

# Поиск по ключевому слову
async def find_keyword(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.keyword)

    keyboard = await inline.back()
    text = await book.find("keyword")
    await call.message.edit_text(text, reply_markup=keyboard)

# Результаты поиска по ключевому слову
async def keyword_results(msg: Message, state: FSMContext):
    await state.clear()

    keyboard = await inline.books("keyword", msg.text)
    text = await book.books("keyword", msg.text)
    await msg.answer(text, reply_markup=keyboard)

# Добавление книги, название книги
async def add_title(call: CallbackQuery, state: FSMContext):
    await state.set_state(States.title)
    keyboard = await inline.back()
    text = await book.add("title")
    await call.message.edit_text(text, reply_markup=keyboard)

# Добавление книги, автор
async def add_author(msg: Message, state: FSMContext):
    if len(msg.text) < 3:
        text = await book.add("error")
        return msg.answer(text)
    await state.update_data(title=msg.text)
    await state.set_state(States.author)
    text = await book.add("author")
    keyboard = await inline.back()
    await msg.answer(text, reply_markup=keyboard)

# Добавление книги, описание
async def add_desc(msg: Message, state: FSMContext):
    if len(msg.text) < 3:
        text = await book.add("error")
        return msg.answer(text)
    await state.update_data(author=msg.text)
    await state.set_state(States.desc)
    text = await book.add("desc")
    keyboard = await inline.back()
    await msg.answer(text, reply_markup=keyboard)

# Добавление книги, жанр
async def add_genre(msg: Message, state: FSMContext):
    if len(msg.text) < 3:
        text = await book.add("error")
        return msg.answer(text)
    await state.update_data(desc=msg.text)
    await state.set_state(States.genre)
    text = await book.add("genre")
    keyboard = await inline.genres("add")
    await msg.answer(text, reply_markup=keyboard)

# Выводим превью книги если кинули жанр сообщением
async def add_preview_text(msg: Message, state: FSMContext):
    if len(msg.text) < 3:
        text = await book.add("error")
        return msg.answer(text)
    await state.update_data(genre=msg.text)
    await state.set_state(States.preview)

    data = await state.get_data()
    book_info = [data["title"], data["author"], data["desc"], data["genre"]]

    text = await book.add("preview", value=book_info)
    keyboard = await inline.confirm()
    await msg.answer(text, reply_markup=keyboard)

# Выводим превью книги если кинули жанр кнопкой
async def add_preview(call: CallbackQuery, state: FSMContext):
    genre = call.data.split("_")[2]
    await state.update_data(genre=genre)
    await state.set_state(States.preview)

    data = await state.get_data()
    book_info = [data["title"], data["author"], data["desc"], data["genre"]]

    text = await book.add("preview", value=book_info)
    keyboard = await inline.confirm()
    await call.message.edit_text(text, reply_markup=keyboard)

# Отправляем всё в бд и даем успешно
async def add_run(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await api.add_book(data["title"], data["author"], data["desc"], data["genre"])
    await state.clear()
    keyboard = await inline.back()
    await call.message.edit_text("✅ Книга успешно добавлена!", reply_markup=keyboard)



router.message.register(start, Command("start"))
router.callback_query.register(call_start, F.data == "start")

router.callback_query.register(books_all, F.data == "books_all")
router.callback_query.register(books_find, F.data == "books_find")
router.callback_query.register(book_info, F.data.startswith("book_"))
router.callback_query.register(book_delete, F.data.startswith("delete_"))

router.callback_query.register(find_genre, F.data == "find_genre")
router.callback_query.register(genre_results, F.data.startswith("genre_"))

router.callback_query.register(find_keyword, F.data == "find_keyword")
router.message.register(keyword_results, States.keyword, F.text)

router.callback_query.register(add_title, F.data == "books_add")
router.message.register(add_author, States.title, F.text)
router.message.register(add_desc, States.author, F.text)
router.message.register(add_genre, States.desc, F.text)
router.callback_query.register(add_preview, States.genre, F.data.startswith("add_genre_"))
router.message.register(add_preview_text, States.genre, F.text)
router.callback_query.register(add_run, States.preview, F.data == "add_confirm")