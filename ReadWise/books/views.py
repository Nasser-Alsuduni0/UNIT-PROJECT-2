from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Book ,Review
from django.db.models import Q

def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all().order_by('-created_at')

    if request.method == 'POST':
        reviewer_name = request.POST.get('reviewer_name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if reviewer_name and rating and comment:
            Review.objects.create(
                book=book,
                reviewer_name=reviewer_name,
                rating=int(rating),
                comment=comment
            )
            return redirect('books:book_detail', book_id=book.pk)

    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews
    })

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

def view_readlist(request):
    readlist_ids = request.session.get('readlist', [])
    books = Book.objects.filter(id__in=readlist_ids)
    return render(request, 'books/readlist.html', {'books': books})

def add_to_readlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    readlist = request.session.get('readlist', [])

    if book_id not in readlist:
        readlist.append(book_id)
        request.session['readlist'] = readlist

    return redirect('books:view_readlist')

def remove_from_readlist(request, book_id):
    readlist = request.session.get('readlist', [])
    if book_id in readlist:
        readlist.remove(book_id)
        request.session['readlist'] = readlist
    return redirect('books:view_readlist')


