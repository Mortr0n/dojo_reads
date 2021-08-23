from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('new', views.new_book),
    path('create', views.create_book),
    path('<int:book_id>', views.view_book),
    path('user/<int:users_id>', views.user),
    path('<int:book_id>/review', views.review),
    path('<int:book_id>/edit_book', views.edit_book),
    path('<int:book_id>/update_book', views.update_book),
    path('<int:book_id>/delete_book', views.delete_book),
    path('<int:book_id>/destroy_book', views.destroy_book),
    path('author_show', views.author_show),
    path('<int:author_id>/edit_author', views.author_edit),
    path('<int:author_id>/author_update', views.author_update),
]
