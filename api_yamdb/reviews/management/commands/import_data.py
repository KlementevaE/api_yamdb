from django.core.management.base import BaseCommand

import csv

from api_yamdb.settings import BASE_DIR
from reviews.models import (
    User, Category,
    Genre, Title,
    TitleGenre, Review, Comment
)

STATIC_DATA = BASE_DIR + r'\static\data'

CATEGORY_FILE = STATIC_DATA + r'\category.csv'
GENRE_FILE = STATIC_DATA + r'\genre.csv'
USERS_FILE = STATIC_DATA + r'\users.csv'
TITLES_FILE = STATIC_DATA + r'\titles.csv'
GENRE_TITLE_FILE = STATIC_DATA + r'\genre_title.csv'
REVIEW_FILE = STATIC_DATA + r'\review.csv'
COMMENT_FILE = STATIC_DATA + r'\comments.csv'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(CATEGORY_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Category.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        with open(GENRE_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Genre.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
        with open(USERS_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = User.objects.get_or_create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6],
                )
        with open(TITLES_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Title.objects.get_or_create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category_id=row[3],
                )
        with open(GENRE_TITLE_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = TitleGenre.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    genre_id=row[2],
                )
        with open(REVIEW_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Review.objects.get_or_create(
                    id=row[0],
                    title_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    score=row[4],
                    pub_date=row[5],
                )

        with open(COMMENT_FILE, 'r', encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                _, created = Comment.objects.get_or_create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author_id=row[3],
                    pub_date=row[4],
                )
