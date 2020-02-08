from django.urls import path, include
from . import views

urlpatterns = [
    # path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('mail_list/', views.email_list, name='email_list'),
    path('mail_write/', views.mail_contents_write, name='email_write'),
    path('mail_detail/<int:pk>', views.mail_contents_detail, name='mail_detail'),
]