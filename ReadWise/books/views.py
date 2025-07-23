from django.shortcuts import render ,get_object_or_404
from .models import Book

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