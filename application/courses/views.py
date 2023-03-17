from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from courses.forms import NewUserForm, StudentProfileForm, QuestionForm, AnswerForm, SubmitForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Course,Notice,Question,Student,Assignment,Submission
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

# Create your views here.

def user_login(request):
   if request.method == "POST":
      username = request.POST['usernameInput']
      password = request.POST['passwordInput']
      user = authenticate(request,username=username,password=password)

      if user is not None:
         login(request,user)
         return redirect('dashboard')

      else:
         messages.error(request, "Invalid Details")
         return redirect('login')
   else:
      return render(request,'authenticate/login.html',{})

def user_logout(request):
   logout(request)
   messages.success(request,"Your were logged out!")
   return redirect("home")

def register_student(request):
   if request.method=="POST":
      user_form = NewUserForm(data = request.POST)
      student_form = StudentProfileForm(data = request.POST)

      if user_form.is_valid() and student_form.is_valid():

         user = user_form.save()
         user.is_student = True
         user.save()
         student = student_form.save(commit=False)
         student.user=user
         student.save()
         login(request, user)
         messages.success(request,"Registration successful!")
         return redirect('dashboard')

      else:
         print(user_form.errors,student_form.errors)
   else:
      user_form = NewUserForm()
      student_form = StudentProfileForm()

   return render(request,'authenticate/register_student.html',{'user_form':user_form,'student_form':student_form})

def dashboard(request):
   courses = Course.objects.all()
   return render(request,"courses/all_courses.html",{'all_courses':courses})

def view_assignments(request,course_id):
   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)

   return render(request,'courses/assignments_details.html',{'course':course,'assignments':assignments})

def submit_assignment(request,course_id,assignment_id):
   #za taj assignment se ovdje radi upload i brisanje submission-a
   student = request.user.Student
   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)
   assignment = get_object_or_404(Assignment,pk=assignment_id)
   submit_form = SubmitForm()

   if request.method == 'GET':
      if 'submitted_button' in request.GET:
         submission = Submission.objects.filter(student=student).filter(assignment=assignment)[:1].get()
         return render(request,'courses/submitted.html',{'course':course,'assignments':assignments,
                                                         'assignment':assignment,'submission':submission})

   elif request.method == 'POST':
      if 'submit_button' in request.POST:
         submit_form = SubmitForm(request.POST, request.FILES)
         if submit_form.is_valid():
            file = request.FILES['file_submission'] #get the uploaded file
            submission = Submission.objects.create(student=student,assignment=assignment,file_submission=file)
            submission.save()
            return render(request,'courses/assignments_details.html',{'course':course,'assignments':assignments})
      elif 'delete_button' in request.POST:
         submission = Submission.objects.filter(student=student).filter(assignment=assignment)[:1].get()
         submission.delete()
         submit_form = SubmitForm()
         return render(request,'courses/submit_assignment.html',{'course':course,'assignments':assignments,
                                                           'assignment':assignment,'submit_form':submit_form})
   else:
      submit_form = SubmitForm()
   return render(request,'courses/submit_assignment.html',{'course':course,'assignments':assignments,
                                                           'assignment':assignment,'submit_form':submit_form})

def view_course(request,course_id,question_id=None):
   course = get_object_or_404(Course,pk=course_id)
   notices = Notice.objects.filter(course=course)
   questions = Question.objects.filter(course=course)
   question_form = QuestionForm()
   answer_form = AnswerForm()

   if request.method=="POST":
      if 'question_button' in request.POST:
         question_form = QuestionForm(data = request.POST)
         answer_form = AnswerForm()

         if question_form.is_valid():
            question = question_form.save(commit=False)
            question.course = course
            question.student = get_object_or_404(Student,pk=request.user.id)
            question.save()
            return render(request,"courses/course.html",{'course':course,'notices':notices,
                          'questions':questions,'question_form':question_form,'answer_form':answer_form})

         else:
            print(question_form.errors)

      if 'reply_button' in request.POST:
         answer_form = AnswerForm(data = request.POST)
         question_form = QuestionForm()

         if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = get_object_or_404(Question,pk=question_id)
            answer.save()
            return render(request,"courses/course.html",{'course':course,'notices':notices,
                          'questions':questions,'question_form':question_form,'answer_form':answer_form})

         else:
            print(answer_form.errors)

   return render(request,"courses/course.html",{'course':course,'notices':notices,
                'questions':questions,'question_form':question_form,'answer_form':answer_form})