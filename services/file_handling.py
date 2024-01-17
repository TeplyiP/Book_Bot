import os
import sys

PAGE_SIZE = 1050

book: dict[int, str] = {}


# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int)->tuple[str,int]:
    simbols={',','.','!',':','?',';',' '}
    substr=text[start:start+size]
    count:int = 0
    for i in reversed(substr):
        if i in simbols:
            return substr[:len(substr)-count],len(substr[:len(substr)-count])
        else:
            count=count+1
    return substr,len(substr)





# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    f = open(path, 'r')
    text=f.read()
    counter:int = 0
    page:int = 1
    while counter<len(text):
        temp_lulip=_get_part_text(text,counter,PAGE_SIZE)
        try:
            book[page]=temp_lulip[0].lstrip()
        except TypeError:
            continue
        page=page+1
        counter=counter+temp_lulip[1]
    f.close()

