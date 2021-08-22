from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('new', views.new_book),
    path('create', views.create_book),
    path('<int:book_id>', views.view_book),
    path('user/<int:users_id>', views.user),
    path('<int:book_id>/review', views.review),
]
