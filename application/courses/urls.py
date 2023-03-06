from django.urls import path
from . import views

urlpatterns = [
    path('register/student', views.register_student,name='register_student'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
]