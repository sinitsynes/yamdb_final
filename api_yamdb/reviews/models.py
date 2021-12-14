from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор')
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='user',
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='title'
    )
    description = models.CharField(
        max_length=1000,
        blank=True,
        verbose_name='Описание произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'title: {self.title}, genre: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Произведение'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10),
        ),
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author'), name='unique_review_author'),
        )
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
