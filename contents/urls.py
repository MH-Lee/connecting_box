from django.urls import path, include
from . import views

urlpatterns = [
    # path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('mail_list/', views.email_list, name='email_list'),
    # path('mail_detail/<int:pk>', views., name='mail_detail'),
]