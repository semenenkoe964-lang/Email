from django.urls import path
from mailapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('set-user/', views.set_user, name='set_user'),
    path('compose/', views.compose_email, name='compose_email'),
    path('folder/<str:folder_name>/', views.email_list, name='email_list'),
    path('email/<int:email_id>/', views.email_detail, name='email_detail'),
    path('email/<int:email_id>/move/', views.move_email, name='move_email'),
    path('email/<int:email_id>/delete/', views.delete_email, name='delete_email'),
]
