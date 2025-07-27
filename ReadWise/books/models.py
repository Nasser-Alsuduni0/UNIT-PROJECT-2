from django.db import models
from utils.supabase_client import upload_to_supabase

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField()
    cover_url = models.URLField(blank=True ,null=True) 
    published_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)  
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_name} - {self.book.title} ({self.rating})"
    

