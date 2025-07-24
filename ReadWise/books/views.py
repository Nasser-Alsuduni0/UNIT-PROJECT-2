from django.shortcuts import render ,get_object_or_404
from .models import Book
from django.db.models import Q

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = book.reviews.select_related('user').order_by('-created_at')

    context = {
        'book': book,
        'reviews': reviews,
    }
    return render(request, 'books/book_detail.html', context)

def search_books(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        results = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    context = {
        'query': query,
        'books': results,
    }
    return render(request, 'books/search_results.html', context)