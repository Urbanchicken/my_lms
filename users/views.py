from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from core.models import BookInstance, Book
from .forms import LoginForm, SignUpForm
from django.views.generic import View
from django.contrib.auth.models import Group

class LoginPageView(View):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username = request.POST['username'],
                password = request.POST['password']
            )
            if user is not None:
                login(request, user)
                return redirect('core:index')
            message = 'login failed'
            return render(request, self.template_name, {'form': form, 'message': message})

class SignUpView(View):
    form_class = SignUpForm
    template_name = 'users/signup.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            role = request.POST['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)
            login(request, user)
            return redirect('core:index')
        return render(request, self.template_name, {'form': form})

def profile(request, id):
    user = CustomUser.objects.get(id=id)
    books = BookInstance.objects.filter(borrower=request.user).order_by('-date_borrowed')
    context = {'user': user, 'books': books}
    return render(request, 'users/profile.html', context)

def signout(request):
    logout(request)
    messages.success(request, "You've been logged out successfully!")
    return redirect('users:login')

def notifications(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        book = Book.objects.get(borrower=request.user)
    except Book.DoesNotExist:
        book=None
    context = {'book': book, 'user': user}
    return render(request, 'users/notifications.html', context)
