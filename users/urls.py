from django.urls import path, include
from.import views
from lms.settings import MEDIA_URL,MEDIA_ROOT, STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

app_name='users'

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('signout/', views.signout, name='signout'),
    path('notifications/<int:id>/', views.notifications, name='notifications'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
