import os
import sys

BOOK_PATH = 'books/book.txt'
PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int)->tuple[str,int]:
    simbols={',','.','!',':','?',';'}
    substr=text[start:start+size]
    count:int = 0
    for i in reversed(substr):
        if i in simbols:
            return substr[:len(substr)-count],len(substr[:len(substr)-count])
        else:
            count=count+1





# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    f = open(path, 'r',encoding="utf-8")
    text=f.read()
    counter:int = 0
    page:int = 1
    while counter<len(text):
        temp_lulip=_get_part_text(text,counter,PAGE_SIZE)
        book[page]=temp_lulip[0].lstrip()
        page=page+1
        counter=counter+temp_lulip[1]
    f.close()

# Вызов функции prepare_book для подготовки книги из текстового файла
prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))