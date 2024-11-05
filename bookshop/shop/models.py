from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    genre = models.ManyToManyField('Genres')
    name = models.CharField('Название книги', max_length=128)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата создания', auto_now=True)
    rating = models.IntegerField('Рейтинг', null=True, blank=True)
    orders_count = models.IntegerField('Кол-во заказов', default=0)
    stock_count = models.IntegerField('Оставшееся кол-во книг', default=0)
    annotations = models.TextField('Описание книги')
    page_count = models.IntegerField('Кол-во страниц')
    published_by = models.CharField('Издательство', max_length=128)
    published_at = models.PositiveIntegerField('Год публикации')
    cover = models.ImageField(upload_to="photos/book/")
    price = models.IntegerField('Цена')

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField('Имя', max_length=256)
    full_name = models.CharField('Полное имя', max_length=1028)
    birthday = models.DateField('Дата рождения')
    discription = models.TextField('Описание')
    photo = models.ImageField(upload_to="photos/author/")
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата создания', auto_now=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField('Название жанра', max_length=128)

    def __str__(self):
        return self.name


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.IntegerField('Цена')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата создания', auto_now=True)
    status = models.CharField('Статус заказа', max_length=128)

    def str(self):
        return self.pk


class OrderedBooks(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.PROTECT)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT)
    amount = models.IntegerField('Кол-во')

    def str(self):
        return self.pk


class ShoppingCart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT)
    amount = models.IntegerField('Кол-во')
    price = models.IntegerField('Цена')

    def str(self):
        return self.pk


class BookRating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    book_id = models.ForeignKey('Book', on_delete=models.PROTECT)
    score = models.IntegerField('Оценка')

    def str(self):
        return self.pk
