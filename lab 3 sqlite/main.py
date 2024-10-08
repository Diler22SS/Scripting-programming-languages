import sqlite3
import requests

URL = "https://jsonplaceholder.typicode.com/posts"


# 1 )Создание базы данных:
conn = sqlite3.connect('posts.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY,
        user_id INTEGER, 
        title TEXT, 
        body TEXT
    )''')


# 2) Получение данных с сервера:
def get_requesr(url):
    response = requests.get(url)
    return response.json()

posts = get_requesr(URL)


# 3) Сохранение данных в базу данных:
for post in posts:
    cursor.execute(f'INSERT INTO posts(user_id, title, body) VALUES ({post["userId"]}, {post["title"]}, {post["body"]})')
conn.commit()


# 4) Чтение данных из базы:
    # Реализуйте функционал чтения данных из базы данных.
cursor.execute('SELECT * FROM posts')
posts_list = cursor.fetchall()
for post in posts_list:
    print(post)


    # Напишите запрос для получения всех постов, 
    # принадлежащих конкретному пользователю (по полю user_id).
user_id = input("Input user_id: ")
cursor.execute(f'SELECT user_id, body FROM Posts WHERE user_id = {user_id}')
posts_list = cursor.fetchall()
for post in posts_list:
    print(post)
    
    
    
conn.close()