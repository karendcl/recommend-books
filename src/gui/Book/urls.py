from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('all_books/', views.load_all_books, name='all_books'),
    path('create_document/', views.create_document, name='create_document'),
    path('recommendations/', views.load_recommendations, name='recommendations')
]
