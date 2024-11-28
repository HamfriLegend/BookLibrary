import json
from enum import Enum
import os
from datetime import datetime
from json import JSONDecodeError
from typing import List
import copy


class Statuses(Enum):
    IN_STOCK = 0
    ISSUED = 1


class Book:
    """
    Класс описывающий модель книги
    """

    def __init__(self, book_id, title, author, year):
        self._id = book_id
        self._title = title
        self._author = author
        self._year = year
        self._status = Statuses.IN_STOCK

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def year(self):
        return self._year

    def __str__(self):
        if self._status == Statuses.IN_STOCK:
            status = "В наличии"
        else:
            status = "Выдана"
        return (f"ID: {self._id}\n"
                f"Название: {self._title}\n"
                f"Автор: {self._author}\n"
                f"Год издания: {self._year}\n"
                f"Статус: {status}")

    def to_dict(self):
        """
        Сериализация для json
        :return: dict(id, title, author, year, status)
        """
        return {
            "id": self._id,
            "title": self._title,
            "author": self._author,
            "year": self._year,
            "status": self._status.value
        }

    def set_status(self, status: Statuses):
        """
        Изменение статуса книги
        :param status: статус
        :return:
        """
        self._status = status


class Library:
    """
    Класс бибилиотеки для работы с книгами (Book)
    """

    def __init__(self, file_name: str):
        """
        :param file_name: название файла для хранения данных
        """
        self._books = []
        if file_name.endswith('.json'):
            self.file_name = file_name
            if not os.path.exists(file_name):
                dir_path = os.path.dirname(file_name) or "."
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                if not os.path.exists(file_name):
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump([], f)

            else:
                try:
                    with open(file_name, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        for book in data:
                            l_book = Book(book['id'], book['title'], book['author'], book['year'])
                            l_book.set_status(Statuses(book['status']))
                            self._books.append(l_book)

                except JSONDecodeError:
                    raise Exception("Неверное содержание JSON файла")
        else:
            raise Exception("Неподдерживаемый тип файла. Только JSON")

    def get_books(self) -> List[Book]:
        """
        Получить список всех книг
        :return: Список книг(Book)
        """
        return copy.deepcopy(self._books)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавление новой книги
        :param title: Название
        :param author: Автор
        :param year: Год
        :return:
        """
        if title.replace(' ', '') == '' or author.replace(' ', '') == '':
            raise ValueError("Название и автор не должны быть пустыми")
        if not (1800 <= year <= datetime.now().year):
            raise ValueError(f"Год должен быть между 1800 и {datetime.now().year}")
        else:
            book_id = self._next_book_id()
            book = Book(book_id, title, author, year)
            self._books.append(book)
            self._save_books()

    def delete_book(self, book_id: int):
        """
        Удаление книги
        :param book_id: id книги
        :return:
        """
        try:
            book = self._get_book(book_id)
        except IndexError:
            raise IndexError(f"Такого ID: {book_id} нет в списке книг")

        self._books.remove(book)
        self._save_books()

    def _next_book_id(self) -> int:
        """
        Генерация следующего ID книги
        :return: уникальный ID
        """
        if len(self._books) == 0:
            max_id = -1
        else:
            max_id = max(book.id for book in self._books)
        return max_id + 1

    def _save_books(self):
        """
        Сохранение книг в файл
        :return:
        """
        books_dict = [book.to_dict() for book in self._books]
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(books_dict, f, ensure_ascii=False)

    def _get_book(self, book_id: int) -> Book:
        return list(filter(lambda book: book.id == book_id, self._books))[0]

    def search_book(self, title: str = "", author: str = "", year: int = 0) -> List[Book]:
        """
        Поиск книг (если параметр не указан, то не используется в поиске
        :param title: Название
        :param author: Автор
        :param year: Год (если 0 то не используется в поиске)
        :return: Список книг (Book)
        """
        if year == 0:
            return copy.deepcopy(list(filter(lambda book:
                                             title in book.title
                                             and author in book.author,
                                             self._books)))
        else:
            return copy.deepcopy(list(filter(lambda book:
                                             title in book.title
                                             and author in book.author
                                             and book.year == year,
                                             self._books)))

    def set_status(self, book_id: int, status: Statuses):
        try:
            book = self._get_book(book_id)
        except IndexError:
            raise IndexError(f"Такого ID: {book_id} нет в списке книг")
        book.set_status(status)
        self._save_books()
