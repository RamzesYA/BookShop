from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('books/', BookView.as_view(), name='books'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book'),
    path('authors/', AuthorView.as_view(), name='authors'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),
    path('cart/', ShoppingCartView.as_view(), name='cart'),
    path('statistic/', StatisticView.as_view(), name='statistic'),
]
