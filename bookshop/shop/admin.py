from django.contrib import admin
from .models import *


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genres)
admin.site.register(Order)
admin.site.register(OrderedBooks)
admin.site.register(ShoppingCart)
admin.site.register(BookRating)
