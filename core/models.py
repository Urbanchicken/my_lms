from django.db import models
from users.models import CustomUser
import uuid
from datetime import datetime

genres = [
    ('SciFi', 'SciFi'),
    ('Romance', 'Romance'),
    ('Thriller', 'Thriller'),
    ('Kids', 'Kids'),
    ('Educational', 'Educational'),
    ('Memoir', 'Memoir'),
    ('Business', 'Business'),
    ('Action', 'Action'),
]

status_choices = [
    ('A', 'Available'),
    ('R', 'Requested'),
    ('T', 'Taken')
]

class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    summary = models.TextField()
    cover_photo = models.ImageField(upload_to="cover_images")
    genre = models.CharField(max_length=20, choices=genres)
    status = models.CharField(max_length=50, choices=status_choices, default='A')
    uuid = models.UUIDField(default=uuid.uuid4)
    borrower = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    date_borrowed = models.DateTimeField(null=True, blank=True, default=None)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    no_borrowed = models.IntegerField(default=0)

    class Meta:
        permissions = (('can_change_status', 'Change the status of the book'),
                        ('can_request_book', 'Can request for a book to borrow'),
                        ('can_return_book', 'Can return a borrowed book'))

    def __str__(self) -> str:
        return self.title

    @property
    def is_due(self):
        return bool(self.status=='T' and datetime.now() > self.due_date)

class BookInstance(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=63)
    publisher = models.CharField(max_length=63)
    borrower = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(null=True, blank=True, default=None)

    def __str__(self):
        return self.title 


