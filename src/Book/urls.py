from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('all_books/', views.load_all_books, name='all_books'),
    path('add_book/', views.create_document, name='add_book'),
    path('recommendations/', views.load_recommendations, name='recommendations'),
    path('update/', views.update, name='update')
]
