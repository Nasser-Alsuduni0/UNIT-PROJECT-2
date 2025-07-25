from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.search_books, name='search_books'), 
    path('<int:book_id>/add-to-readlist/', views.add_to_readlist, name='add_to_readlist'),
    path('readlist/', views.view_readlist, name='view_readlist'),
    path('readlist/remove/<int:book_id>/', views.remove_from_readlist, name='remove_from_readlist'),
]