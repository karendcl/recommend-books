from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, 'main.html')