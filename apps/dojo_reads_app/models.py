from django.db import models
from apps.login_registration_app.models import User



class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # books_written
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books_written', on_delete=models.CASCADE)
    # review = models.TextField()
    # reviewed_by = models.ManyToManyField(User, related_name='books_reviewed')
    added_by = models.ForeignKey(User, related_name='books_added', on_delete=models.CASCADE)
    # rating = models.DecimalField(max_digits=1, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Review(models.Model):
    content = models.TextField()
    reviewed_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    book_reviewed = models.ForeignKey(Book, related_name='review', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
