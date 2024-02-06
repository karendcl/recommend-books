from django.shortcuts import render, HttpResponse
#send a message to the user
from django.contrib import messages
from .models import Book
import requests
import json

from pathlib import Path
import os, sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#Add another file that is outside of the project
sys.path.append(os.path.join(BASE_DIR, 'code'))
import trial

def create_document(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        title = request.POST.get('title')
        author = request.POST.get('author')
        img = request.POST.get('img')

        book = Book(title=title, author=author, image_url=img, description=text)

        try:
            book.save()
            messages.success(request, 'Document created successfully')
        except:
            messages.error(request, 'Document already exists')
            return render(request, 'create_book.html')


    return render(request, 'create_book.html')

def load_all_books(request):
    books = Book.objects.all()
    return render(request, 'ViewBooks.html', {'books': books})

def load_recommendations(request):
    if request.method == 'POST':

        books = request.POST.getlist('books')
        books = [int(book) for book in books]
        suggestions = trial.make_suggestion(books)

        scor = suggestions[1]
        suggestions = suggestions[0]

        #map the suggestions to the books
        suggestions = [i+1 for i in suggestions]
        suggestions = [Book.objects.get(id=suggestion) for suggestion in suggestions]



        print(suggestions)

        messages.success(request, 'Recommendations created successfully')

        scores = {}
        for i in range(len(suggestions)):
            scores[i] = scor[i]

        print(scores)


        return render(request, 'Recommended.html', {'suggestions': suggestions, 'scores': scores})

    else:
        return render(request, 'ViewBooks.html')

def update(request):
    if request.method =='POST':
        allbooks = Book.objects.all()
        texts = [i.description for i in allbooks]
        trial.update(texts)
        messages.success(request, 'Model updated successfully')
        return render(request, 'ViewBooks.html',{'books': allbooks})
    return render(request, 'HomePage.html')

def plot(request):
    trial.plot_scatter_clusters()
