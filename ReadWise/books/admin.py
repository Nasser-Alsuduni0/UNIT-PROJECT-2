from django.contrib import admin
from django import forms
from .models import Book, Genre, Review
from utils.supabase_client import upload_to_supabase

class BookForm(forms.ModelForm):
    cover_upload = forms.ImageField(required=False, label="Cover Image")

    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'description', 'published_date', 'cover_upload']

class BookAdmin(admin.ModelAdmin):
    form = BookForm

    def save_model(self, request, obj, form, change):
        cover_file = form.cleaned_data.get('cover_upload')
        if cover_file:
            supabase_url = upload_to_supabase(cover_file)
            obj.cover_url = supabase_url
        super().save_model(request, obj, form, change)

admin.site.register(Book, BookAdmin)
admin.site.register(Genre)
admin.site.register(Review)

