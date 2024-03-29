from django.urls import path
from . import views

urlpatterns = [
    path('register/student',views.register_student,name='register_student'),
    path('login',views.user_login,name='login'),
    path('logout',views.user_logout,name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('my_courses',views.my_courses,name='my_courses'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('tutor_course/<int:course_id>',views.view_tutor_course,name='tutor_course'),
    path('tutor_course/<int:course_id>/questions',views.view_questions_tutor,name='view_questions_tutor'),
    path('tutor_course/<int:course_id>/questions/<int:question_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('tutor_course/<int:course_id>/<int:post_id>',views.view_tutor_course,name='tutor_course'),
    path('course/<int:course_id>',views.view_course,name='course'),
    path('course/<int:course_id>/overview',views.overview,name='overview'),
    path('course/<int:course_id>/questions',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/questions/<int:question_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/questions/<int:question_id>/<int:answer_id>',views.view_questions_tutor,name='view_questions_tutor'),
    path('course/<int:course_id>/assignment_overview',views.assignment_overview,name='assignment_overview'),
    path('course/<int:course_id>/assignments',views.view_assignments,name='assignments'),
    path('tutor_course/<int:course_id>/assignments',views.view_assignments,name='assignments'),
    path('tutor_course/<int:course_id>/students',views.view_students,name='view_students'),
    path('course/<int:course_id>/assignments/<int:assignment_id>',views.submit_assignment,name='submit_assignment'),
    path('tutor_course/<int:course_id>/assignments/<int:assignment_id>',views.view_submissions,name='view_submissions'),
    path('tutor_course/<int:course_id>/assignments/<int:assignment_id>/<int:submission_id>',views.view_submissions,name='view_submissions'),
]