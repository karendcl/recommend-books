from django.contrib import admin

# Register your models here.

#register the book model
from .models import Book

admin.site.register(Book)