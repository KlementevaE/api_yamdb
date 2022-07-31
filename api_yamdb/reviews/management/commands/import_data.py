from django.core.management.base import BaseCommand

import csv
import re

from api_yamdb.settings import BASE_DIR
from reviews.models import (
    User, Category,
    Genre, Title,
    TitleGenre, Review, Comment
)


STATIC_DATA = BASE_DIR + r'/static/data'

CATEGORY_FILE = STATIC_DATA + r'/category.csv'
GENRE_FILE = STATIC_DATA + r'/genre.csv'
USERS_FILE = STATIC_DATA + r'/users.csv'
TITLES_FILE = STATIC_DATA + r'/titles.csv'
GENRE_TITLE_FILE = STATIC_DATA + r'/genre_title.csv'
REVIEW_FILE = STATIC_DATA + r'/review.csv'
COMMENT_FILE = STATIC_DATA + r'/comments.csv'


FILES = {
    Category: CATEGORY_FILE,
    Genre: GENRE_FILE,
    User: USERS_FILE,
    Title: TITLES_FILE,
    TitleGenre: GENRE_TITLE_FILE,
    Review: REVIEW_FILE,
    Comment: COMMENT_FILE,
}


def read_from_csv(model, datafile):
    with open(datafile, 'r', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Две строки с re.sub нужны в связи с тем,
            # что в csv-файлах не везде корректно названы стобцы
            row = {re.sub(r'(category)$',
                          'category_id', k): v for (k, v) in row.items()}
            row = {re.sub(r'(author)$',
                          'author_id', k): v for (k, v) in row.items()}
            _, created = model.objects.get_or_create(**row)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for model, datafile in FILES.items():
            read_from_csv(model, datafile)
