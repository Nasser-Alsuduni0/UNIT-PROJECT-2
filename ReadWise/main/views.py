from django.shortcuts import render
from books.models import Book, Review

def home(request):
    recent_reviews = Review.objects.select_related('book').order_by('-created_at')[:3]
    popular_books = Book.objects.all().order_by('-created_at')[:4]  

    context = {
        'recent_reviews': recent_reviews,
        'popular_books': popular_books,
    }
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')
