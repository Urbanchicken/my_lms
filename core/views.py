from django.shortcuts import render, redirect
from .models import Book, BookInstance
from django.contrib.auth.decorators import login_required, permission_required
from .forms import BookForm
from django.contrib import messages 
from datetime import datetime, timedelta, timezone
import pytz 

def index(request):
    return render(request, 'core/index.html', {})

@login_required
def catalog(request):
    books = Book.objects.all()
    number = Book.objects.count()
    context = {'books':books, 'number': number} 
    return render(request, "core/catalog.html", context)

@login_required
def details(request, uuid):
    book = Book.objects.get(uuid=uuid) 
    userr = None
    if book.status != 'A':
        if book.borrower == request.user:
            userr = request.user
        else:
            context = {'book': book, 'userr': userr}
            return render(request, 'core/details.html', context)
    context = {'book': book, 'userr': userr}
    return render(request, 'core/details.html', context)

@login_required
@permission_required('core.can_request_book')
def request_book(request, uuid):
    book = Book.objects.get(uuid=uuid)
    try:
        book2 = Book.objects.get(borrower=request.user)
    except Book.DoesNotExist:
        book.borrower = request.user
        book.status = 'R'
        book.save()
        return redirect("core:details", uuid=book.uuid)
    else:
        messages.info(request, "Please return the last book you borrowed before borrowing another!")
        return redirect("core:details", uuid=book.uuid)

@login_required
@permission_required('core.add_book')
def new_book(request):
    if request.method != 'POST':
        form = BookForm()
    else:
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('core:index')
    context = {'form': form}
    return render(request, 'core/new_book.html', context)
    

@login_required
@permission_required('core.can_return_book')
def return_book(request, uuid):
    book = Book.objects.get(uuid=uuid)
    book.status = 'A'
    book.borrower = None
    book.no_borrowed += 1
    book.due_date = None
    book.date_borrowed = None
    book.save()
    return redirect('core:details', uuid=book.uuid)

@login_required
@permission_required('core.can_change_status')
def take_book(request, uuid):
    book = Book.objects.get(uuid=uuid)
    book.status = 'T'
    borrow_time = datetime.now().replace(tzinfo=timezone.utc)
    book.date_borrowed = borrow_time
    book.due_date = book.date_borrowed + timedelta(minutes=5)
    print(book.due_date)
    book.save()
    new_inst = BookInstance.objects.create(title=book.title, author=book.author, publisher=book.publisher, borrower=book.borrower, date_borrowed=datetime.now())
    return redirect('core:details', uuid=book.uuid)

def searched(request):
    if request.method == 'POST':
        required = request.POST['search']
        others = None
        try:
            book = Book.objects.get(title__contains=required)
        except Book.DoesNotExist:
            book = None
        else:
            others = Book.objects.filter(genre=book.genre)
        context = {'book': book, 'others': others}
        return render(request, 'core/searched.html', context)




