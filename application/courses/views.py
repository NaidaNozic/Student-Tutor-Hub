from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from courses.forms import NewUserForm,StudentProfileForm,QuestionForm,AnswerForm,SubmitForm,PostForm,MaterialForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Course,Notice,Question,Student,Assignment,Submission,TutorCourse,Tutor,Material,Answer
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
   newUser=request.user
   if newUser.is_tutor:
      tutor_courses=TutorCourse.objects.filter(tutor=newUser.Tutor)
      courses=[x.course for x in tutor_courses]
      return render(request,"courses/all_courses.html",{'all_courses':courses})
   else:
      courses = Course.objects.all()
   return render(request,"courses/all_courses.html",{'all_courses':courses})

def view_assignments(request,course_id):
   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)

   return render(request,'courses/assignments_details.html',{'course':course,'assignments':assignments})

def assignment_overview(request,course_id):
   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)

   return render(request,'courses/assignments.html',{'course':course,'assignments':assignments})

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

def view_tutor_course(request,course_id,post_id=None):
   course = get_object_or_404(Course,pk=course_id)
   notices = Notice.objects.filter(course=course)
   post_form = PostForm()
   material_form = MaterialForm()

   if request.method=='POST':
      if 'post_button' in request.POST:
         post_form = PostForm(data = request.POST)
         material_form = MaterialForm(request.POST, request.FILES)
         
         if post_form.is_valid() and material_form.is_valid():
            post = post_form.save(commit=False)
            post.tutor = get_object_or_404(Tutor,pk=request.user.id)
            post.course = course
            post.save()
            file = request.FILES.get('material', False)
            if file:
               material = Material.objects.create(notice=post,material=file)
               material.save()
            return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})
         else:
            print(post_form.errors)

      elif 'delete_post_button' in request.POST:
         notice = get_object_or_404(Notice,pk=post_id)
         Material.objects.filter(notice=notice).delete()
         notice.delete()
         notices = Notice.objects.filter(course=course)
         return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})

   return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})

#For both tutors and students
def view_questions_tutor(request,course_id,question_id=None,answer_id=None):
   course = get_object_or_404(Course,pk=course_id)
   questions = Question.objects.filter(course=course)

   question_form = QuestionForm()
   answer_form = AnswerForm()

   if request.method=='POST':

      if 'question_button' in request.POST:
         question_form = QuestionForm(data = request.POST)

         if question_form.is_valid():
            question = question_form.save(commit=False)
            question.course = course
            question.user=request.user
            question.save()
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
         else:
            print(question_form.errors)

      elif 'reply_button' in request.POST:
         answer_form = AnswerForm(data = request.POST)

         if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = get_object_or_404(Question,pk=question_id)
            answer.save()
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
         else:
            print(answer_form.errors)

      elif 'delete_question_button' in request.POST:
         question = get_object_or_404(Question,pk=question_id)
         question.delete()
         questions = Question.objects.filter(course=course)
         return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
      elif 'delete_answer_button' in request.POST:
         answer = get_object_or_404(Answer,pk=answer_id)
         answer.delete()
         return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})

   return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                                      'question_form':question_form,'answer_form':answer_form})


def view_course(request,course_id,question_id=None):
   course = get_object_or_404(Course,pk=course_id)
   notices = Notice.objects.filter(course=course)

   return render(request,"courses/course.html",{'course':course,'notices':notices})