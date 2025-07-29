from django.shortcuts import render, redirect
from books.models import Book, Review
from .models import ContactMessage

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
    message_sent = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            message_sent = True

    return render(request, 'main/contact.html', {
        'message_sent': message_sent
    })

