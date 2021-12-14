import csv
import io

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

User = get_user_model()


class Command(BaseCommand):
    help = 'Заполняет БД данными'

    def load_users(self):
        with io.open(
            'static/data/users.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                )

    def load_categories(self):
        with io.open(
            'static/data/category.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                Category.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug'],
                )

    def load_genres(self):
        with io.open(
            'static/data/genre.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                Genre.objects.get_or_create(
                    name=row['name'],
                    slug=row['slug'],
                )

    def load_titles(self):
        with io.open(
            'static/data/titles.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    name=row['name'],
                    year=row['year'],
                    category=category,
                )

    def load_title_genres(self):
        with io.open(
            'static/data/genre_title.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                genre = Genre.objects.get(id=row['genre_id'])
                title = Title.objects.get(id=row['title_id'])
                TitleGenre.objects.get_or_create(
                    genre=genre,
                    title=title,
                )

    def load_reviews(self):
        with io.open(
            'static/data/review.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                title = Title.objects.get(id=row['title'])
                author = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    title=title,
                    text=row['text'],
                    author=author,
                    score=row['score'],
                )

    def load_comments(self):
        with io.open(
            'static/data/comments.csv',
            mode='r',
            encoding='utf-8'
        ) as f:
            reader = csv.DictReader(f, dialect='excel')
            for row in reader:
                review = Review.objects.get(id=row['review'])
                author = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    review=review,
                    text=row['text'],
                    author=author,
                )

    def handle(self, *args, **kwargs):
        self.load_users()
        self.load_categories()
        self.load_genres()
        self.load_titles()
        self.load_title_genres()
        self.load_reviews()
        self.load_comments()
