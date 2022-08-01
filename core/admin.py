from django.contrib import admin
from .models import Book, BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'title', 'author', 'status')
    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'publisher', 'no_borrowed')
        }),
        ('Details', {
                'fields': ('uuid', 'genre', 'cover_photo')
            }),
        ('Availability', {
            'fields': ['status',
                        ('borrower', 'date_borrowed')]
        }),
        ('Return', {
            'fields': ('due_date',)
        }),
        ('Brief', {
            'fields': ('summary',)
        })
    )
    list_filter = ('status', 'due_date')

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('title', 'borrower', 'date_borrowed')
