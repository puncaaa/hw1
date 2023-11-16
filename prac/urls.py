from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from newstable import views
from newstable.views import nt_list, nt_detail, create_nt, create_comment, delete_nt, delete_comment, edit_nt, \
    login_view, logout_view, register, confirm_email

urlpatterns = [
    path('', nt_list, name='nt_list'),
    path('nt/<int:pk>/', nt_detail, name='nt_detail'),
    path('nt/create/', create_nt, name='create_nt'),
    path('nt/<int:pk>/edit/', edit_nt, name='edit_nt'),
    path('nt/<int:pk>/comment/', create_comment, name='create_comment'),
    path('nt/<int:pk>/delete/', delete_nt, name='delete_nt'),
    path('comment/<int:pk>/delete/', delete_comment, name='delete_comment'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
]

