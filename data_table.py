import psycopg2 as pg
import json

#создаю таблицу с уникальными идентификаторами, айди вк и столбцом фото, который будет содержать ссылки на фото.
def create_db():
    with pg.connect(database='hw_db_postgres', user='hw', password='511213', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('create table if not exists Users(id serial primary key, vkid varchar(20) not null, photos text[]);')
        conn.commit()

#Возвращаю 10 случайный строк из колонки, беру из них айди вк и фото, переписываю в словарь
def get_random_people():
    dict = {}
    with pg.connect(database='hw_db_postgres', user='hw', password='511213', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        cur.execute('select vkid, photos from Users order by random() limit 10;')
        for item in cur.fetchall():
            dict[item[0]] = item[1]
        return dict

#добавляю всех юзеров в таблицу из JSON, полученного в dump_to_json() в main.py
def add_user(json_file):
    with open(json_file, encoding='utf-8') as file:
        data = json.load(file)
    with pg.connect(database='hw_db_postgres', user='hw', password='511213', host='localhost', port=5432) as conn:
        cur = conn.cursor()
        for key, value in data.items():
            cur.execute('insert into Users(vkid, photos) values (%s, %s);', (key, value))


