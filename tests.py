import unittest
from unittest.mock import patch, mock_open
from datetime import datetime

# Подключение ваших классов
from library import Library, Book, Statuses


class TestLibrary(unittest.TestCase):

    @patch("library.open", new_callable=mock_open, read_data='[]')  # Мокаем open для чтения файла
    def test_library_initialization_empty_file(self, mock_file):
        # Инициализация библиотеки с пустым файлом
        lib = Library("test_books.json")
        self.assertEqual(len(lib.get_books()), 0)  # Должно быть 0 книг

    @patch("library.open", new_callable=mock_open, read_data='[{"id": 1, "title": "Book1", "author": "Author1", "year": 2000, "status": 0}]')
    def test_library_initialization_with_books(self, mock_file):
        # Инициализация библиотеки с книгами
        lib = Library("test_books.json")
        books = lib.get_books()
        self.assertEqual(len(books), 1)  # Должна быть 1 книга
        self.assertEqual(books[0].id, 1)
        self.assertEqual(books[0].title, "Book1")

    @patch("library.open", new_callable=mock_open, read_data='[]')
    def test_add_book_valid(self, mock_file):
        # Проверка добавления книги
        lib = Library("test_books.json")
        lib.add_book("New Book", "New Author", 2020)
        books = lib.get_books()
        self.assertEqual(len(books), 1)  # Должна быть 1 книга
        self.assertEqual(books[0].title, "New Book")
        self.assertEqual(books[0].author, "New Author")
        self.assertEqual(books[0].year, 2020)

    def test_add_book_invalid_title(self):
        # Проверка ошибки при добавлении книги с пустым названием
        lib = Library("test_books.json")
        with self.assertRaises(ValueError):
            lib.add_book("", "New Author", 2020)

    def test_add_book_invalid_year(self):
        # Проверка ошибки при добавлении книги с неверным годом
        lib = Library("test_books.json")
        with self.assertRaises(ValueError):
            lib.add_book("New Book", "New Author", 1700)

    @patch("library.open", new_callable=mock_open, read_data='[{"id": 1, "title": "Book1", "author": "Author1", "year": 2000, "status": 0}]')
    def test_delete_book_valid(self, mock_file):
        # Проверка удаления книги
        lib = Library("test_books.json")
        lib.delete_book(1)
        books = lib.get_books()
        self.assertEqual(len(books), 0)  # Книга должна быть удалена

    @patch("library.open", new_callable=mock_open, read_data='[{"id": 1, "title": "Book1", "author": "Author1", "year": 2000, "status": 0}]')
    def test_delete_book_invalid_id(self, mock_file):
        # Проверка ошибки при удалении книги с несуществующим id
        lib = Library("test_books.json")
        with self.assertRaises(Exception):
            lib.delete_book(999)  # Нет книги с id 999
    @patch("library.open", new_callable=mock_open,
           read_data='[{"id": 1, "title": "Book1", "author": "Author1", "year": 2000, "status": 0},{"id": 2, '
                     '"title": "Book2", "author": "Author2", "year": 2001, "status": 1}]')
    def test_search_book(self, mock_file):
        # Проверка поиска книги
        lib = Library("test_books.json")
        lib.add_book("New Book999", "New Author", 2020)
        result = lib.search_book(title="New Book999")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].title, "New Book999")

        result = lib.search_book(title="Book1", author="Author2")
        self.assertEqual(len(result), 0)
        result = lib.search_book(title="Book2", author="Author2")
        self.assertEqual(len(result), 1)
        result = lib.search_book(title="Book", author="Author")
        self.assertEqual(len(result), 3)
        result = lib.search_book(year=2000)
        self.assertEqual(len(result), 1)

    @patch("library.open", new_callable=mock_open, read_data='[]')
    def test_set_status(self, mock_file):
        # Проверка изменения статуса книги
        lib = Library("test/test_books.json")
        lib.add_book("New Book", "New Author", 2020)
        book = lib.get_books()[0]
        self.assertEqual(book._status, Statuses.IN_STOCK)

        lib.set_status(book.id, Statuses.ISSUED)
        book = lib.get_books()[0]
        self.assertEqual(book._status, Statuses.ISSUED)

    @patch("library.open", new_callable=mock_open, read_data='[{"id": 1, "title": "Book1", "author": "Author1", "year": 2000, "status": 0}]')
    def test_next_book_id(self, mock_file):
        # Проверка генерации следующего ID
        lib = Library("test_books.json")
        next_id = lib._next_book_id()
        self.assertEqual(next_id, 2)  # Максимальный id был 1, следующий должен быть 2

    def test_invalid_file_extension(self):
        # Проверка исключения при неправильном расширении файла
        with self.assertRaises(Exception):
            lib = Library("test_books.txt")  # Неправильный формат файла


if __name__ == "__main__":
    unittest.main()
