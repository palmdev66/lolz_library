import sqlite3

conn = sqlite3.connect("books.db", check_same_thread=False)

# Генерируем БД
async def generate():
    cur = conn.cursor()
    try:
        cur.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, desc BIGTEXT, genre TEXT)')
        cur.execute('CREATE TABLE IF NOT EXISTS genres (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        conn.commit()
        cur.execute('SELECT * FROM genres')
        if cur.fetchall():
            return
        genres = ["Эпос", "Лирика", "Драма", "Детектив"]
        for genre in genres:
            cur.execute('INSERT INTO genres (name) VALUES (?)', (genre, ))
        conn.commit()
    except Exception as e:
        print(e)

# Получить все книги
async def get_books():
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM books')
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)

# Получить все жанры
async def get_genres():
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM genres')
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)

# Поиск книги по автору/названию
async def find_books_keyword(text):
    cur = conn.cursor()
    text = text.lower()
    try:
        cur.execute('SELECT * FROM books WHERE LOWER(author) LIKE "%" || ? || "%" OR LOWER(title) LIKE "%" || ? || "%"', (text, text,))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)

# Получить подробную информацию о книге
async def get_book_info(id):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM books WHERE id = ?', (id, ))
        result = cur.fetchone()
        return result
    except Exception as e:
        print(e)
    
# Получить книги по жанру
async def find_books_genre(name):
    cur = conn.cursor()
    try:
        cur.execute('SELECT * FROM books WHERE genre = ?', (name, ))
        result = cur.fetchall()
        return result
    except Exception as e:
        print(e)
    
# Добавить книгу
async def add_book(title, author, desc, genre):
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO books (title, author, desc, genre) VALUES (?, ?, ?, ?)', (title, author, desc, genre))
        conn.commit()

        cur = cur.execute('SELECT * FROM genres WHERE name = ?', (genre, ))
        result = cur.fetchone()

        if not result:
            cur.execute('INSERT INTO genres (name) VALUES (?)', (genre, ))
            conn.commit()
    except Exception as e:
        print(e)

# Удалить книгу
async def remove_book(id):
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM books WHERE id = ?', (id, ))
        conn.commit()
    except Exception as e:
        print(e)