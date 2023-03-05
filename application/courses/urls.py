from django.urls import path
from . import views

urlpatterns = [
    path('register/student', views.register_student,name='register_student'),
    path('login',views.user_login,name='login'),
]