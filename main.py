from library import Library, Statuses
import os
def clear_console():
    if os.name == 'nt':  # Если Windows
        os.system('cls')
    else:  # Для Linux и macOS
        os.system('clear')



while True:
    file_name = input("Введите путь к файлу JSON с книгами (если файла нет, он создастся автоматически: ")
    try:
        lib = Library(file_name)
        while True:
            command = input("Выберите команду:\n"
                            "1. Добавить книгу\n"
                            "2. Удалить книгу\n"
                            "3. Поиск книг\n"
                            "4. Вывести список книг\n"
                            "5. Изменить статус книги\n"
                            "6. Выход\n"
                            "Команда: ")


            match command:
                case("1"):
                    clear_console()
                    title = input("Введите название книги: ")
                    author = input("Введите автора книги: ")
                    year = input("Введите год издания книги: ")
                    try:
                        year = int(year)
                        try:
                            lib.add_book(title, author, year)
                            print("Книга добавлена!")
                        except ValueError as e:
                            print(e)

                    except ValueError:
                        print("Год введен некорректно")
                case("2"):
                    clear_console()
                    book_id = input("Введите ID книги: ")
                    try:
                        book_id = int(book_id)
                        try:
                            lib.delete_book(book_id)
                            print("Книга удалена!")
                        except IndexError as e:
                            print(e)

                    except ValueError:
                        print("ID введен некорректно")

                case("3"):
                    clear_console()
                    print("Оставьте поле пустым, если не хотите выполнять по нему поиск!")
                    title = input("Введите название книги: ")
                    author = input("Введите автора книги: ")
                    year = input("Введите год издания книги: ")
                    try:
                        if year != '':
                            year = int(year)
                        else:
                            year = 0
                        try:
                            books = lib.search_book(title, author, year)
                            if len(books) == 0:
                                print("Книг не найдено!")
                            else:
                                print(f"Найдено {len(books)} книг.")
                            for book in books:
                                print(book)
                                print("-"*15)

                        except ValueError as e:
                            print(e)

                    except ValueError:
                        print("Год введен некорректно")
                case("4"):
                    clear_console()
                    books = lib.get_books()
                    if len(books) == 0:
                        print("Книг нет!")
                    for book in books:
                        print(book)
                        print("-"*15)

                case("5"):
                    clear_console()
                    book_id = input("Введите ID книги: ")
                    status = input("Выберите статус: 0 - В наличии | 1 - Выдана\nСтатус: ")
                    try:
                        book_id = int(book_id)
                        status = int(status)
                        if status not in (0, 1):
                            raise ValueError

                        try:
                            lib.set_status(book_id, Statuses(status))
                            print("Статус книги обновлен!")
                        except IndexError as e:
                            print(e)
                    except ValueError:
                        print("ID или Статус введен некорректно")

                case("6"):
                    break

                case _:
                    clear_console()
                    print("Нет такой команды")

        break
    except Exception as e:
        print(e)

