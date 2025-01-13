from django.shortcuts import render

def home(request):
    return render(request, 'kargo/home.html')

def nosotros(request):
    return render(request, 'kargo/nosotros.html')

def galeria(request):
    return render(request, 'kargo/galeria.html')