from xml.dom.minidom import Document
from django.urls import path
from . import views
from lms.settings import MEDIA_URL,MEDIA_ROOT, STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('book/<str:uuid>/',views.details,name='details'),
    path('request_book/<str:uuid>/', views.request_book, name='request_book'),
    path('new_book/', views.new_book, name='new_book'),
    path('return_book/<str:uuid>/', views.return_book, name='return_book'),
    path('take_book/<str:uuid>/', views.take_book, name='take_book'),
    path('searched/', views.searched, name='searched'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)