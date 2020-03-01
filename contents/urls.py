from django.urls import path, include
from . import views
from .api.views import RescueAPIView


urlpatterns = [
    # path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('mail_list/', views.email_list, name='email_list'),
    path('mail_write/', views.mail_contents_write, name='email_write'),
    path('mail_detail/<int:pk>', views.mail_contents_detail, name='mail_detail'),

    path('table/', views.all_table),

    path('pd_list/', views.professor_dev_list, name='professor_dev_list'),
    path('pd_write/', views.professor_dev_write, name='professor_dev_write'),
    path('su_list/', views.start_up_list, name='start_up_list'),
    path('su_write/', views.start_up_write, name='start_up_write'),
    path('fr_list/', views.finance_report_list, name='finance_report_list'),
    path('fr_write/', views.finance_report_write, name='finance_report_write'),

    # 회생기업 숨긴 list
    path('api/rescue/', RescueAPIView.as_view(), name='rescue_api'),
    path('rescue_list/', views.rescue_list, name='rescue_list'),
    path('rescue_detail/<int:pk>/', views.rescue_detail, name='rescue_detail'),
]