# Проект YaMDb
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: "Книги", "Фильмы", "Музыка".
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы и выставляют произведению рейтинг.

### Ресурсы API YaMDb
**AUTH**: аутентификация.

**USERS**: пользователи.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Алгоритм регистрации пользователей
Пользователь отправляет POST-запрос с параметром email на `/api/v1/auth/email/`.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email (функция в разработке).
Пользователь отправляет POST-запрос с параметрами email и confirmation_code на `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен).
Эти операции выполняются один раз, при регистрации пользователя. В результате пользователь получает токен и может работать с API, отправляя этот токен с каждым запросом.

### Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

### Технологии

- Python 3.8.10
- Django 2.2.19
- Django REST Framework 3.12.4
- Simple-JWT 4.7.2

### Установка
Склонируйте репозиторий. Находясь в папке с кодом создайте виртуальное окружение `python -m venv venv`, активируйте его (Windows: `source venv\scripts\activate`; Linux/Mac: `sorce venv/bin/activate`), установите зависимости `python -m pip install -r requirements.txt`.

Для запуска сервера разработки,  находясь в директории проекта выполните команды:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Проект запущен и доступен по адресу [localhost:8000](http://localhost:8000/).

### Авторы
Павел Новиков, Клементьева Евгения, Рустам Магомедов
