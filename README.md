# yamdb_final
проект доступен по адресу: 51.250.18.91
![Django-app workflow](https://github.com/sinitsynes/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


# Yatube API


Сервис для работы с Yatube через другие приложения. Поддерживает CRUD для создания постов и комментариев к ним, просмотр данных о сообществе, позволяет подписаться и просмотреть подписки пользователя. Авторизация происходит с помощью JWT, пакет включен в список требований.

## Примеры запросов

Работа программы доступна только авторизованным пользователям. Для входа в систему необходимо отправить POST-запросом по адресу '/api/v1/jwt/create/' уже действующую связку логина и пароля в формате JSON, в ответ придут токены JWT для доступа к сервису ("access") и для получения нового ("refresh"). Токен доступа должен находиться в заголовке запроса с ключом "Authorization" и значением "Bearer {token}".

```
POST
{"username":"example_user",
"password":"example_password"}

GET
{"refresh":"refresh-token",
"access":"access-token"}
```

Запрос авторизованного пользователя на /posts/ 
```
{
  "text": "string",
  "group": 0
}
```

создаст запись:

```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2021-08-26T13:14:36.579Z",
  "image": "string",
  "group": 0
}
```

Комментарий можно оставить направив POST-запрос на /posts/{post_id}/comments/ c указанием номера поста:
```
{
  "text": "string"
}
```

Подписка осуществляется по имени пользователя:
```
POST:

{
  "following": "username"
}

GET:
[
    {
        "user": "example_user1",
        "following": "example_user2"
    }
]
```

# Локальная установка

Скачать проект, создать и активировать виртуальное окружение, установить зависимости из api_yamdb/requirements.txt
```
pip install -r requirements.txt
```
Применить миграции
```
python manage.py migrate
```
И запуск сервера:
```
python manage.py runserver
```
