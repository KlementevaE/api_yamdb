import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLE_CHOICES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(max_length=9,
                            choices=ROLE_CHOICES,
                            default='user')
    confirmation_code = models.CharField(
        'Confirmation code',
        max_length=4,
        blank=True,
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name="Название категории")
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name="Slug категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['-pk']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name="Название жанра")
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name="Slug жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['-pk']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название произведения")
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(dt.datetime.now().year)],
        verbose_name="Год выпуска")
    description = models.TextField(
        blank=True,
        verbose_name="Описание")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name="Slug категории")
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        through='TitleGenre',
        verbose_name="Slug жанра")

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ['-pk']

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titlegenres',
        verbose_name="ID произведения"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="ID жанра"
    )

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"
        ordering = ['-pk']
        constraints = [
            models.UniqueConstraint(fields=['title', 'genre'],
                                    name='unique_connection'),
        ]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(
        verbose_name='Отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка произведения')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_connection'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')
    text = models.TextField(
        verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария')

    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий на отзыв'
        verbose_name_plural = 'Комментарии на отзывы'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
