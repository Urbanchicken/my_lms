from django import forms 
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'cover_photo', 'genre', 'summary']
        labels = {'title': 'Title', 'author': 'Author', 'publisher': 'Publisher', 
                    'cover_photo': 'Cover Photo', 'genre': 'Genre', 'summary': 'Summary'}
        