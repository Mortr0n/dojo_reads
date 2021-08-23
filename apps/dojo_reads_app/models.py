from django.db import models
from apps.login_registration_app.models import User
from django.http import request

class Author_Manager(models.Manager):
    def author_validator(self, post_data):
        errors = {}
        if len(post_data['author']) < 2:
            errors['name'] = 'Name must be at least 2 characters'
        if Author.objects.filter(name = post_data['author']):
            errors['same_name'] = 'Author name already exists'
        return errors
    
class Book_Manager(models.Manager):
    def book_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 2:
            errors['title'] = 'Title must be at least 2 characters'
        if Book.objects.filter(title = post_data['title']):
            errors['same_title'] = 'There is already a book with that title'
        return errors
    
class Review_Manager(models.Manager):
    def review_validator(self, post_data):
        errors = {}
        if len(post_data['content']) < 10:
            errors['content'] = 'A review must be at least 10 characters long.'
        return errors
        



class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # books_written
    objects = Author_Manager()
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books_written', on_delete=models.CASCADE)
    # review = models.TextField()
    # reviewed_by = models.ManyToManyField(User, related_name='books_reviewed')
    added_by = models.ForeignKey(User, related_name='books_added', on_delete=models.CASCADE)
    # rating = models.DecimalField(max_digits=1, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Book_Manager()
    
class Review(models.Model):
    content = models.TextField()
    reviewed_by = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    book_reviewed = models.ForeignKey(Book, related_name='review', on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=1, decimal_places=0, default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Review_Manager()
    
