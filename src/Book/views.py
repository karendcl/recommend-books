from django.shortcuts import render, HttpResponse
#send a message to the user
from django.contrib import messages
from .models import Book

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

        book = Book(title=title, author=author, image_url=img)

        try:
            #get highest id
            pd = Book.objects.latest('id').id +1
            trial.Add_New_Document(text, pd)
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
        print(books)
        books = [int(book) for book in books]
        suggestions = trial.make_suggestion(books)

        #map the suggestions to the books
        suggestions = [Book.objects.get(id=suggestion) for suggestion in suggestions]

        return render(request, 'Recommended.html', {'suggestions': suggestions})

    else:
        return render(request, 'ViewBooks.html')