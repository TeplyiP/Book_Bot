import sqlite3 as sql


def check_id_in_base(us_id: int)->bool:
    existing:bool = False
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    cur.execute(f'SELECT user_id FROM users WHERE user_id = {us_id}')
    existing = cur.fetchone()
    cur.close()
    conn.close()
    if existing is None:
        return False
    else:
        return True

def add_user(us_id:int, username:str):
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    insert_param="""INSERT INTO users(user_id,user_full_name,page,book_name)
    VALUES(?,?,?,?);"""
    data_tuple=(us_id,username,1,'book')
    cur.execute(insert_param,data_tuple)
    conn.commit()
    cur.close()
    conn.close()

def get_page_text(p_num: int, table_name:str)->str:
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=(f'SELECT page_text FROM ' + table_name + f' WHERE page_num = {p_num}')
    cur.execute(temp)
    result=cur.fetchone()
    if result is not None: # если не последняя страница
        cur.close()
        conn.close()
        return result[0]        
    else: #если последняя страница
        cur.close()
        conn.close()
        return result
        

def get_current_page(user_id:int)->int:
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    cur.execute(f'SELECT page FROM users WHERE user_id = {user_id}')
    result=cur.fetchone()[0]
    cur.close()
    conn.close()
    return result
    

def get_total_pages(table_name: str)->int:
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=('SELECT COUNT(*) FROM ' + table_name)
    cur.execute(temp)
    result=cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

# получаем имя текущей таблицы книги у юзера 
def get_table_name(user_id:int)->str: 
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=(f'SELECT book_name FROM users WHERE user_id = {user_id}')
    cur.execute(temp)
    result=cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

def increment_current_page(user_id:int):
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    cur_p=get_current_page(user_id)
    cur_p=cur_p+1
    temp=(f'UPDATE users SET page={cur_p} WHERE user_id = {user_id}')
    cur.execute(temp)
    conn.commit()
    cur.close()
    conn.close()

def decrement_current_page(user_id:int):
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    cur_p=get_current_page(user_id)
    cur_p=cur_p-1
    temp=(f'UPDATE users SET page={cur_p} WHERE user_id = {user_id}')
    cur.execute(temp)
    conn.commit()
    cur.close()
    conn.close()


#получаем список книг и список названий таблиц в виде списка
#получаем библиотеку
def get_lib_dict()->list:
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=('SELECT book_name,table_name FROM library')
    cur.execute(temp)
    len_tbl=cur.fetchall()
    return len_tbl

def get_tabel_names_for_handler ()->list:
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=('SELECT table_name FROM library')
    cur.execute(temp)
    len_tbl=cur.fetchall()
    result=list()
    for k in len_tbl:
        result.append(k[0])
    cur.close()
    conn.close()
    return result

def set_user_book(user_id:int,table_name:str):
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=('UPDATE users SET book_name = ?,page = ? WHERE user_id = ?')
    cur.execute(temp,(table_name,1,user_id))
    conn.commit()
    cur.close()
    conn.close()

def reset_cur_page_to_1(user_id:int):
    conn=sql.connect('foo.db')
    cur=conn.cursor()
    temp=('UPDATE users SET page = ? WHERE user_id = ?')
    cur.execute(temp,(1,user_id))
    conn.commit()
    cur.close()
    conn.close()