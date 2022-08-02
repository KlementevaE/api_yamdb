from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


ROLE_CHOICES = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', blank=False, unique=True)
    bio = models.TextField(verbose_name='Биография', blank=True)
    role = models.CharField(verbose_name="Роль",
                            max_length=30,
                            choices=ROLE_CHOICES,
                            default=USER)
    confirmation_code = models.CharField(verbose_name='Код подтверждения',
                                         max_length=4,
                                         blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['-pk']

    def __str__(self):
        return self.username
