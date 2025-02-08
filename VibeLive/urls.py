from django.urls import path
from VibeLive import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('signin/', views.signin, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('meeting/', views.meeting, name='meeting'),
    path('joinroom/', views.join_room, name='joinroom'),
    path('logout/', views.logout_view, name='logout'),
]
