from django.contrib import admin

# Register your models here.

from .models import RestaurantLocation, Author, Book

admin.site.register(RestaurantLocation)
admin.site.register(Author)
admin.site.register(Book)