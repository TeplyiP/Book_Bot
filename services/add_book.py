import file_handling as fh
import sqlite3
import os
import sys


BOOK_PATH = 'books/dochka.txt'

# Вызов функции prepare_book для подготовки книги из текстового файла
fh.prepare_book(BOOK_PATH)


#функция добавления книги в базу
def add_book_to_base(table_name: str, book_name: str):
    conn=sqlite3.connect('foo.db')
    cur=conn.cursor()
    pn: int = 1
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ( \
        page integer primary key autoincrement, \
        page_text TEXT, page_num integer)')
    for p in fh.book.values():
        insert_param=(f'INSERT INTO {table_name}(page_text,page_num) VALUES ( ?,? )')
        data_tuple=(p,pn)
        cur.execute(insert_param,data_tuple)
        pn=pn+1
    insert_param=('INSERT INTO library (book_name,table_name) VALUES(?,?) ' )
    data_tuple=(book_name,table_name)
    cur.execute(insert_param,data_tuple)
    conn.commit()
    cur.close()
    conn.close()

add_book_to_base('dochka','Капитанская дочка. А.Пушкин')