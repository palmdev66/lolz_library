from utils import db as api

async def start(fullname):
    return(
        f"📘 Добро пожаловать в библиотеку, *{fullname}*\n\n"
        "Только не шуми сильно.."
    )

async def info(book_id):
    book = await api.get_book_info(book_id)
    title = book[1]
    author = book[2]
    desc = book[3]
    genre = book[4]
    return(
        f"📘 Информация о книге\n\n"
        f"Название: *{title}*\n"
        f"Автор: *{author}*\n"
        f"Жанр: *{genre}*\n"
        f"Описание: *{desc}*"
    )

async def find(key):
    if key == "select":
        return(
            f"🔎 Поиск книг\n\n"
            "Каким методом будем искать?"
        )
    if key == "genre":
        return(
            f"🔎 Поиск книг\n\n"
            "Выберите жанр книги"
        )
    if key == "keyword":
        return(
            f"🔎 Поиск книг\n\n"
            "Введите слово для поиска по автору или названию книги"
        )
    
async def add(key, value=None):
    if key == "title":
        return(
            f"📗 Новая книга\n\n"
            "Укажите название книги"
        )
    if key == "author":
        return(
            f"📗 Новая книга\n\n"
            "Укажите автора книги"
        )
    if key == "desc":
        return(
            f"📗 Новая книга\n\n"
            "Укажите описание книги"
        )
    if key == "genre":
        return(
            f"📗 Новая книга\n\n"
            "Выберите жанр из уже предложенных, или напишите свой"
        )
    if key == "preview":
        return(
            f"📗 Проверьте все данные о книге\n\n"
            f"Название: *{value[0]}*\n"
            f"Автор: *{value[1]}*\n"
            f"Описание: *{value[2]}*\n"
            f"Жанр: *{value[3]}*"
        )
    if key == "error":
        return(
            "❌ Длина текста должна быть не менее 3-х символов"
        )

async def books(filter=None, key=None):
    if not filter:
        books = await api.get_books()
    if filter == "keyword":
        books = await api.find_books_keyword(key)
    if filter == "genre":
        books = await api.find_books_genre(key)

    if not books:
        return(
            f"🔎 Книги не найдены :("
        )
    
    count = len(books)
    return(
            f"🔎 Найдено книг: {count}"
        )