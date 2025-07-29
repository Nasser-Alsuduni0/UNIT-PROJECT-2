from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Book ,Review
from django.db.models import Q
import requests
from dotenv import load_dotenv
import os
import math

load_dotenv()


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
    query = request.GET.get('q', '').strip()
    books = []
    api_books = []

    if query:
   
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        ).order_by('-created_at')

        
        if not books.exists():
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_BOOKS_API_KEY not found in .env file")

            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                "q": f"intitle:{query}",
                "maxResults": 12,
                "key": api_key
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    volume_info = item.get("volumeInfo", {})
                    api_books.append({
                        "title": volume_info.get("title", "Unknown Title"),
                        "author": ", ".join(volume_info.get("authors", [])),
                        "description": volume_info.get("description", "No description available."),
                        "cover_url": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                        "link": volume_info.get("infoLink", "#"),
                        "rating": volume_info.get("averageRating", "N/A"),
                        "pages": volume_info.get("pageCount", "N/A"),
                        "published": volume_info.get("publishedDate", "N/A"),
                    })

    return render(request, 'books/search_results.html', {
        'query': query,
        'books': books,        
        'api_books': api_books 
    })


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


def discover_books(request):
    

    category = request.GET.get('category', 'science')
    page = int(request.GET.get('page', 1))
    max_results = 12
    start_index = (page - 1) * max_results
    min_rating = request.GET.get('min_rating')
    rating_options = ['5', '4', '3', '2', '1']

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    category_options = [
        'science', 'history', 'art', 'romance',
        'biography', 'technology', 'sports', 'mystery'
    ]

    query = f"subject:{category}"

    params = {
        "q": query,
        "maxResults": max_results,
        "startIndex": start_index,
        "key": api_key
    }

    response = requests.get("https://www.googleapis.com/books/v1/volumes", params=params)
    api_books = []
    total_items = 0

    if response.status_code == 200:
        data = response.json()
        total_items = data.get("totalItems", 0)

        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail", "")
            
            rating = volume_info.get("averageRating")
            if min_rating and rating:
             try:
                 if float(rating) < float(min_rating):
                     continue
             except ValueError:
                 continue

            api_books.append({
                "title": volume_info.get("title", "No title"),
                "author": ", ".join(volume_info.get("authors", [])),
                "description": volume_info.get("description", "No description."),
                "cover_url": thumbnail,
                "link": volume_info.get("infoLink", "#"),
                "rating": volume_info.get("averageRating", "N/A"),
                "pages": volume_info.get("pageCount", "N/A"),
                "published": volume_info.get("publishedDate", "N/A"),
                "rating": rating or "N/A",
            })

    total_pages = math.ceil(total_items / max_results)
    start_page = max(page - 2, 1)
    end_page = min(start_page + 4, total_pages)
    start_page = max(end_page - 4, 1)
    page_range = range(start_page, end_page + 1)

    return render(request, 'books/discover_books.html', {
        'api_books': api_books,
        'selected_category': category,
        'category_options': category_options,
        'page': page,
        'total_pages': total_pages,
        'page_range': page_range,
        'min_rating': min_rating,
        'rating_options': rating_options,
    })