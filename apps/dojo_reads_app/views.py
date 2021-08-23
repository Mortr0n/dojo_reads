from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from apps.login_registration_app.models import User
from .models import Book, Author, Review

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    # Grabbing the last three books added to the list for the most recent list
    last_three = Review.objects.all().order_by('-created_at')[:3]
    all_books = Book.objects.all()
    context = {
        'this_user' : User.objects.filter(id=request.session['user_id'])[0],
        'recent_reviews' : last_three,
        'all_books' : all_books
    }
    return render(request, 'home.html', context)

def new_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_user' : User.objects.filter(id=request.session['user_id'])[0],
        'authors' : Author.objects.all()
    }
    return render(request, 'new_book.html', context)

def create_book(request):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    # If theres an author selected go with that one.  If not go with whatever is in the author field
    if request.POST['author_select'] == "none":
        this_author = Author.objects.create(name=request.POST['author'])
    else:
        this_author = Author.objects.filter(id=request.POST['author_select'])[0]
    new_book = Book.objects.create(
        title=request.POST['title'],
        author = this_author,
        added_by = this_user,        
    )
    new_review = Review.objects.create(
        content = request.POST['review'],
        reviewed_by = this_user,
        book_reviewed = new_book,
        rating = request.POST['rating']
    )
    # adding this user as a reviewer immediately since they are adding the book and a review
    # new_book.reviewed_by.add(this_user)
    return redirect(f'/dojo/{new_book.id}')

def view_book(request, book_id):
    this_book = Book.objects.filter(id=book_id)[0]
    context = {
        'this_book' : this_book,
        'all_reviews' : Review.objects.filter(book_reviewed=this_book)
    }
    return render(request, 'view_book.html', context)

def user(request, users_id):
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    displayed_user = User.objects.filter(id=users_id)[0]
    last_three = Review.objects.filter(reviewed_by=displayed_user).order_by('-created_at')[:3]
    context = {
        'this_user' : this_user,
        'displayed_user' : displayed_user,
        'displayed_user_reviews' : Review.objects.filter(reviewed_by = this_user.id),
        'last_three' : last_three,
    }
    return render(request, 'users.html', context)

def review(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book = Book.objects.filter(id=book_id)[0]
    new_review = Review.objects.create(
        content = request.POST['review'],
        reviewed_by = this_user,
        book_reviewed = this_book,
        rating = request.POST['rating']        
    )
    return redirect(f'/dojo/{book_id}')