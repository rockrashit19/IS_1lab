# Лабораторная работа №1 — Разработка защищённого REST API

## Описание проекта

Проект представляет собой защищённое REST API, реализованное на языке **Python** с использованием **Flask** и **Flask-JWT-Extended**.  
Приложение демонстрирует базовую архитектуру безопасного веб-сервиса: регистрацию, аутентификацию по JWT и доступ к защищённым ресурсам.  
В коде реализованы меры защиты от распространённых уязвимостей (SQL Injection, XSS), а также автоматический анализ безопасности в CI/CD.

---

## API — доступные эндпоинты

| Метод  | Путь             | Назначение                        | Требует JWT |
| ------ | ---------------- | --------------------------------- | ----------- |
| `POST` | `/auth/register` | Регистрация нового пользователя   | ❌          |
| `POST` | `/auth/login`    | Аутентификация и получение токена | ❌          |
| `GET`  | `/api/data`      | Доступ к защищённым данным        | ✅          |

---

### `POST /auth/register`

**Описание:** создание нового пользователя.  
**Пример запроса:**

```json
{
  "username": "alice",
  "password": "S3cretPass!"
}
```

**Пример ответа (201 Created):**

```json
{
  "msg": "user created",
  "user": {
    "username": "alice"
  }
}
```

### `POST /auth/login`

**Описание:** вход пользователя и получение JWT-токена.
**Пример запроса:**

```json
{
  "username": "alice",
  "password": "S3cretPass!"
}
```

**Пример ответа (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "username": "alice"
  }
}
```

### `GET /api/data`

**Описание:** возвращает защищённые данные для авторизованных пользователей.
**Заголовок:**
Authorization: Bearer <access_token>

**Пример ответа:**

```json
{
  "user": {
    "id": 1,
    "username": "alice"
  },
  "data": [
    {
      "id": 1,
      "title": "Public post 1",
      "content": "Hello &lt;script&gt;alert(1)&lt;/script&gt; from user data"
    },
    {
      "id": 2,
      "title": "Public post 2",
      "content": "This content is safe to render in client"
    }
  ]
}
```

## Реализованные меры защиты

### Защита от SQL Injection

- Используется ORM SQLAlchemy, которая генерирует безопасные SQL-запросы с параметризацией.
- Ни один SQL-запрос не формируется вручную через конкатенацию строк.
- Пример безопасного кода:

```python
user = User.query.filter_by(username=username).first()
```

SQLAlchemy подставляет параметры корректно, исключая инъекцию.

### Защита от XSS (Cross-Site Scripting)

- Все пользовательские данные, которые отображаются в ответах API, экранируются с помощью:

```python
from markupsafe import escape
```

- Вредоносный ввод вроде <script>alert(1)</script> преобразуется в:

```perl
&lt;script&gt;alert(1)&lt;/script&gt;
```

что предотвращает выполнение JavaScript-кода на стороне клиента.

### Безопасная аутентификация и хранение паролей

- Хэширование паролей реализовано с использованием bcrypt из пакета passlib:

```python
from passlib.hash import bcrypt
password_hash = bcrypt.hash(password)
bcrypt.verify(password, user.password_hash)
```

- Аутентификация выполняется через JWT-токены (Flask-JWT-Extended):

```python
access_token = create_access_token(identity=str(user.id))
```

- SECRET_KEY используется для внутренней подписи Flask, JWT_SECRET_KEY — для подписи JWT-токенов.
- Доступ к защищённым маршрутам обеспечивается декоратором @jwt_required().
