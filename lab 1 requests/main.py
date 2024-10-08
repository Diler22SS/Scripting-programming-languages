"""
Задание:
Используя язык программирования python реализовать взаимодейтсвие с тестовым сервером (https://jsonplaceholder.typicode.com/).
1) GET - запрос:
Запросить с тестового сервера список доступных постов и вывести в консоль все посты, пренадлежащие пользователям с чётными id.

2) POST - запрос:
Создать пост с заголовком "Тестовый пост", остальные поля заполняются самостоятельно, в консоль вывести сформированный JSON

3) PUT - запрос
Обновить ранее созданный пост, заменить заголовок на "Обновлённый пост", в консоль вывести обновлённый JSON.
"""

import requests

"""# 1) GET - запрос: Запросить с тестового сервера список доступных постов и 
вывести в консоль все посты, пренадлежащие пользователям с чётными id."""

task_1_requests = requests.get('https://jsonplaceholder.typicode.com/posts')

for record in task_1_requests.json():
  if record['userId']%2==0:
    print(record)

"""# 2) POST - запрос: Создать пост с заголовком "Тестовый пост", остальные 
поля заполняются самостоятельно, в консоль вывести сформированный JSON"""

data = {
    'title': 'Тестовый пост',
    'body': 'Тестовый пост тело',
    'userId': 1,
}

task_2_request = requests.post('https://jsonplaceholder.typicode.com/posts', data=data)

print(task_2_request.json())

"""# 3) PUT - запрос Обновить ранее созданный пост, заменить заголовок на 
"Обновлённый пост", в консоль вывести обновлённый JSON."""

data = {
    'id': 101,
    'title': 'Обновлённый пост',
    'body': 'Обновлённый пост тело',
    'userId': 1,
}

task_3_requests = requests.put('https://jsonplaceholder.typicode.com/posts/1', data=data)

print(task_3_requests.json())