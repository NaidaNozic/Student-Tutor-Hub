from django.urls import path
from . import views

urlpatterns = [
    path('register/student',views.register_student,name='register_student'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('tutor_course/<int:course_id>',views.view_tutor_course,name='tutor_course'),
    path('tutor_course/<int:course_id>/questions',views.view_questions_tutor,name='view_questions_tutor'),
    path('tutor_course/<int:course_id>/questions/<int:question_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('tutor_course/<int:course_id>/<int:post_id>',views.view_tutor_course,name='tutor_course'),
    path('course/<int:course_id>',views.view_course,name='course'),
    path('course/<int:course_id>/questions',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/questions/<int:question_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/questions/<int:question_id>/<int:answer_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/assignment_overview',views.assignment_overview,name='assignment_overview'),
    path('course/<int:course_id>/assignments',views.view_assignments,name='assignments'),
    path('course/<int:course_id>/assignments/<int:assignment_id>',views.submit_assignment,name='submit_assignment'),
]