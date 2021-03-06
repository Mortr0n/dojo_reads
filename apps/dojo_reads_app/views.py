from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from apps.login_registration_app.models import User
from .models import Book, Author, Review
from django.contrib import messages

def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    # Grabbing the last three books added to the list for the most recent list
    last_three = Review.objects.all().order_by('-created_at')[:3]
    all_books = Book.objects.all().order_by('-created_at')
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
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dojo/new')
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
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book = Book.objects.filter(id=book_id)[0]
    context = {
        'this_book' : this_book,
        'all_reviews' : Review.objects.filter(book_reviewed=this_book),
        'this_user' : this_user,
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
    errors = Review.objects.review_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dojo/{book_id}')
    
    this_user = User.objects.filter(id=request.session['user_id'])[0]
    this_book = Book.objects.filter(id=book_id)[0]
    new_review = Review.objects.create(
        content = request.POST['content'],
        reviewed_by = this_user,
        book_reviewed = this_book,
        rating = request.POST['rating']        
    )
    return redirect(f'/dojo/{book_id}')

def edit_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0] #TODO: decide if this is needed at some point
    this_book = Book.objects.filter(id=book_id)[0] 
    context = {
        'this_book' : this_book,
        'all_authors' : Author.objects.all(),
    }
    return render(request, 'update_book.html', context)
    
def update_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request.value)
        return redirect(f'/dojo/{book_id}')
    this_book = Book.objects.filter(id=book_id)[0] 
    this_author = Author.objects.filter(id=request.POST['author_select'])[0]
    this_book.title = request.POST['title']
    this_book.author = this_author
    this_book.save()
    return redirect(f'/dojo/{book_id}')

def delete_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])[0] #TODO: decide if this is needed at some point
    this_book = Book.objects.filter(id=book_id)[0]
    context = {
        'this_book' : this_book,
    }
    return render(request, 'delete_book.html', context)

def destroy_book(request, book_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    this_book = Book.objects.filter(id=book_id)[0]
    this_book.delete()
    return redirect('/dojo')

def author_show(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'all_authors' : Author.objects.all()
    }
    return render(request, 'author_list.html', context)

def author_edit(request, author_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'this_author' : Author.objects.filter(id=author_id)[0],
    }
    return render(request, 'edit_author.html', context)

def author_update(request, author_id):
    if 'user_id' not in request.session and request.method != 'POST':
        return redirect('/')
    errors = Author.objects.author_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dojo/{author_id}/edit_author')
    this_author = Author.objects.filter(id=author_id)[0]
    this_author.name = request.POST['author']
    this_author.save()
    return redirect('/dojo/author_show')

# TODO: Make Edit and Delete Reviews if the user is the logged in user