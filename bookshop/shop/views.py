import json
from datetime import date, datetime, timedelta, timezone

from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from shop.forms import LoginUserForm
from shop.models import *
import re


def home(request):
    return redirect('books')


class BookView(ListView):
    model = Book
    template_name = 'shop/books.html'
    context_object_name = 'books'
    extra_context = {'title': 'Каталог книг'}


class BookDetail(DetailView):
    model = Book
    template_name = 'shop/book.html'
    context_object_name = 'book'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['israte'] = BookRating.objects.filter(user_id=self.request.user, book_id=Book.objects.get(pk=self.kwargs['pk'])).exists()

        sc = ShoppingCart.objects.filter(user_id=self.request.user)
        for i in range(sc.count()):
            print(sc[i].amount)
        return dict(list(context.items()))

    def post(self, request, pk):
        if 'stock_count' in request.POST:
            book_id = Book.objects.get(pk=self.kwargs['pk'])
            amount = self.request.POST.get("stock_count")
            price = Book.objects.get(pk=self.kwargs['pk']).price

            scart = ShoppingCart()
            scart.user_id = self.request.user
            scart.book_id = book_id
            scart.amount = amount
            scart.price = int(price) * int(amount)
            scart.save()

            book = Book.objects.get(pk=self.kwargs['pk'])
            book.stock_count -= int(amount)
            book.save()

            return redirect('/')

        elif 'rating' in request.POST:

            br = BookRating()
            br.user_id = self.request.user
            br.book_id = Book.objects.get(pk=self.kwargs['pk'])
            br.score = self.request.POST.get("rating")
            br.save()

            total_rating = BookRating.objects.filter(book_id=Book.objects.get(pk=self.kwargs['pk'])).aggregate(total_score=Sum('score'))['total_score']
            count_rating = BookRating.objects.filter(book_id=Book.objects.get(pk=self.kwargs['pk'])).count()
            if count_rating > 0:
                rating = round(total_rating/count_rating)
            else:
                rating = 0

            book = Book.objects.get(pk=self.kwargs['pk'])
            book.rating = rating
            book.save()

            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AuthorView(ListView):
    model = Author
    template_name = 'shop/authors.html'
    context_object_name = 'authors'
    extra_context = {'title': 'Авторы'}


class AuthorDetail(DetailView):
    model = Author
    template_name = 'shop/author.html'
    context_object_name = 'author'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'shop/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shop/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ShoppingCartView(ListView):
    model = ShoppingCart
    template_name = 'shop/cart.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = ShoppingCart.objects.filter(user_id=self.request.user)
        context['total'] = ShoppingCart.objects.filter(user_id=self.request.user).aggregate(total_price=Sum('price'))
        sc = ShoppingCart.objects.filter(user_id=self.request.user)

        sc = ShoppingCart.objects.filter(user_id=self.request.user)
        for i in range(sc.count()):
            print(sc[i].amount)
        return dict(list(context.items()))

    def post(self, request):
        order = Order()
        order.user_id = self.request.user
        order.price = ShoppingCart.objects.filter(user_id=self.request.user).aggregate(total_price=Sum('price'))['total_price']
        order.status = 'Заказ оформлен и ожидает отправки'
        order.save()

        sc = ShoppingCart.objects.filter(user_id=self.request.user)

        for i in range(sc.count()):
            order1 = OrderedBooks()
            order1.order_id = order
            order1.book_id = sc[i].book_id
            order1.amount = sc[i].amount
            order1.save()

            book = Book.objects.get(pk=sc[i].book_id.id)
            book.orders_count += sc[i].amount
            book.save()

        scart = ShoppingCart.objects.filter(user_id=self.request.user)
        scart.delete()

        return redirect('/')


class ProfileView(DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'shop/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ord'] = []
        for i in Order.objects.filter(user_id=context['object']).order_by('-created_at'):
            context['ord'].append({'order_id': i.pk,
                                   'ba': OrderedBooks.objects.filter(order_id=i.pk),
                                   'status': i.status,
                                   'price': i.price,
                                   'date': i.created_at})
        return dict(list(context.items()))

    def post(self, request, username):
        mail = self.request.POST.get("mail")
        fName = self.request.POST.get("fName")
        sName = self.request.POST.get("sName")

        u = User.objects.get(username=username)

        if mail and mail != 'Введите почту' and mail != u.email:
            u.email = mail

        pattern = r'^[а-яА-ЯёЁ]+$'
        if re.fullmatch(pattern, fName) and fName != 'Введите имя' and fName != u.first_name:
            u.first_name = fName

        if re.fullmatch(pattern, sName) and sName != 'Введите фамилию' and sName != u.last_name:
            u.last_name = sName

        u.save()

        return redirect('profile', username)


def get_statistics_for_year():
    today = datetime.now().date()

    orders = Order.objects.filter(created_at__year=today.year)

    labels = []
    order_counts = []
    total_amounts = []

    for month in range(1, 13):
        labels.append(str(month))

        order_counts.append(orders.filter(created_at__month=month).count())
        total_amounts.append(
            orders.filter(created_at__month=month).aggregate(total_price=Sum('price'))['total_price'] or 0)

    return labels, order_counts, total_amounts


def get_statistics_for_month():
    today = datetime.now().date()

    orders = Order.objects.filter(created_at__month=today.month, created_at__year=today.year)

    labels = []
    order_counts = []
    total_amounts = []

    for day in range(1, today.day + 1):
        labels.append(str(day))

        order_counts.append(orders.filter(created_at__day=day).count())
        total_amounts.append(
            orders.filter(created_at__day=day).aggregate(total_price=Sum('price'))['total_price'] or 0)

    return labels, order_counts, total_amounts


def get_statistics_for_day():
    today = datetime.now().date()

    orders = Order.objects.filter(created_at__date=today)

    labels = []
    order_counts = []
    total_amounts = []

    for hour in range(0, 24):
        labels.append(str(hour) + ':00')

        order_counts.append(orders.filter(created_at__hour=hour).count())
        total_amounts.append(
            orders.filter(created_at__hour=hour).aggregate(total_price=Sum('price'))['total_price'] or 0)

    return labels, order_counts, total_amounts


class StatisticView(TemplateView):
    template_name = 'shop/statistic.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'period' in self.request.GET:
            period = self.request.GET.get('period')
            labels = order_counts = total_amounts = get_statistics_for_day()

            if period == 'day':
                labels, order_counts, total_amounts = get_statistics_for_day()
            elif period == 'month':
                labels, order_counts, total_amounts = get_statistics_for_month()
            elif period == 'year':
                labels, order_counts, total_amounts = get_statistics_for_year()

            context['data'] = {
                'labels': labels,
                'order_counts': order_counts,
                'total_amounts': total_amounts
            }
            return dict(list(context.items()))
        if 'period' in self.request.GET:
            period = self.request.GET.get('period')
            labels = order_counts = total_amounts = get_statistics_for_day()

            if period == 'day':
                labels, order_counts, total_amounts = get_statistics_for_day()
            elif period == 'month':
                labels, order_counts, total_amounts = get_statistics_for_month()
            elif period == 'year':
                labels, order_counts, total_amounts = get_statistics_for_year()

            context['data'] = {
                'labels': labels,
                'order_counts': order_counts,
                'total_amounts': total_amounts
            }
            return dict(list(context.items()))
