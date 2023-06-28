from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from courses.forms import NewUserForm,StudentProfileForm,QuestionForm,AnswerForm,SubmitForm,PostForm,MaterialForm,AssignmentForm,UserUpdateForm,UpdateSubmissionForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Course,Notice,Question,Student,Assignment,Submission,TutorCourse,Tutor,Material,Answer,NewUser,StudentCourse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required


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

@login_required
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

@login_required
def my_courses(request):

   if request.user.is_tutor:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   student_courses = StudentCourse.objects.filter(student=request.user.Student)
   courses=[x.course for x in student_courses]

   return render(request,"courses/all_courses.html",{'all_courses':courses})

@login_required
def dashboard(request):
   newUser=request.user
   if newUser.is_tutor:
      tutor_courses=TutorCourse.objects.filter(tutor=newUser.Tutor)
      courses=[x.course for x in tutor_courses]
      return render(request,"courses/all_courses.html",{'all_courses':courses})
   else:
      courses = Course.objects.all()
   return render(request,"courses/all_courses.html",{'all_courses':courses})

@login_required
def profile(request,pk):

   user_form = UserUpdateForm()

   if request.method=='POST':
      user = get_object_or_404(NewUser,pk=pk)

      if 'update_user_button' in request.POST:
         user_form = UserUpdateForm(data = request.POST)
         if user_form.is_valid():
            email= user_form.cleaned_data.get("email")
            first_name= user_form.cleaned_data.get("first_name")
            last_name= user_form.cleaned_data.get("last_name")
            phone= user_form.cleaned_data.get("phone")
            if email:
               user.email = email
            if first_name:
               user.first_name = first_name
            if last_name:
               user.last_name = last_name
            if phone:
               if request.user.is_tutor:
                  tutor = get_object_or_404(Tutor,pk=request.user.id)
                  tutor.phone = phone
                  tutor.save()
               else:
                  student = get_object_or_404(Student,pk=request.user.id)
                  student.phone = phone
                  student.save()
            user.save()
            messages.success(request,"Update successful!")
            user_form = UserUpdateForm()

            return render(request,'courses/profile.html',{'user_form':user_form})

         else:
            print(user_form.errors.as_data())
            messages.warning(request,'Error')

   return render(request,'courses/profile.html',{'user_form':user_form})

@login_required
def view_assignments(request,course_id):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)

   return render(request,'courses/assignments_details.html',{'course':course,'assignments':assignments})

@login_required
def overview(request,course_id):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)

   if request.method=='POST':
      if 'withdraw_button' in request.POST:
         user_id = request.POST.get('withdraw_button')
         newUser = get_object_or_404(NewUser,pk=user_id)
         student_course_objects = StudentCourse.objects.filter(course=course,student=newUser.Student)
         student_course_objects.delete()
         messages.success(request,'Successfull withdraw!')

         tutors = Tutor.objects.filter(course=course)
         return render(request,"courses/enroll.html",{'course':course,'tutors':tutors})

   tutors = Tutor.objects.filter(course=course)
   
   return render(request,'courses/overview.html',{'course':course,'tutors':tutors})

@login_required
def view_students(request,course_id):

   if request.user.is_student:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')
   elif is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)

   if request.method == 'POST':
      if 'remove_student_button' in request.POST:
         student_id = request.POST.get('remove_student_button')
         student = get_object_or_404(Student,pk=student_id)
         student_course_objects = StudentCourse.objects.filter(course=course,student=student)
         student_course_objects.delete()
         messages.success(request, 'Student removed successfully!')

   student_course_objects = StudentCourse.objects.filter(course=course)
   students = [x.student for x in student_course_objects]

   return render(request,'courses/students.html',{'course':course,'students':students})

@login_required
def assignment_overview(request,course_id):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)
   assignments = Assignment.objects.filter(course=course)
   assignment_form = AssignmentForm()

   if request.method == 'POST':
      if 'assignment_upload_button' in request.POST:
         assignment_form = AssignmentForm(request.POST, request.FILES)
         if assignment_form.is_valid():
            file = request.FILES['file_assignment']
            assignment = assignment_form.save(commit=False)
            assignment.tutor = request.user.Tutor
            assignment.course = course
            assignment.file_assignment=file
            assignment.save()

            assignment_form = AssignmentForm()
            assignments = Assignment.objects.filter(course=course)
            assignment_form = AssignmentForm()
            return render(request,'courses/assignments.html',{'course':course,'assignments':assignments,'assignment_form':assignment_form})
         else:
            print(assignment_form.errors)
            messages.warning(request,"Error posting the assignment!")
            return render(request,'courses/assignments.html',{'course':course,'assignments':assignments,'assignment_form':assignment_form})

   return render(request,'courses/assignments.html',{'course':course,'assignments':assignments,'assignment_form':assignment_form})

@login_required
def view_submissions(request,course_id,assignment_id,submission_id=None):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')
   elif request.user.is_student:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)
   assignment = get_object_or_404(Assignment,pk=assignment_id)
   submissions = Submission.objects.filter(assignment=assignment)
   submission_form = UpdateSubmissionForm()

   if request.method=='POST':
      if 'assignment_delete_button' in request.POST:
         assignment.file_assignment.delete()
         assignment.delete()
         assignment_form = AssignmentForm()
         assignments = Assignment.objects.filter(course=course)
         return render(request,'courses/assignments.html',{'course':course,'assignments':assignments,'assignment_form':assignment_form,
                                                            'submission_form':submission_form})
      elif 'grade_button' in request.POST:
         submission_form = UpdateSubmissionForm(data = request.POST)
         if submission_form.is_valid():
            grade = submission_form.cleaned_data['grade']
            submission = get_object_or_404(Submission,pk=submission_id)
            if grade:
               submission.grade = grade
            submission.save()
            messages.success(request,"You have successfully graded a student assignment!")
            submission_form = UpdateSubmissionForm()
            return render(request,'courses/submissions.html',{'course':course,'submissions':submissions,
                                                              'submission_form':submission_form})

   return render(request,'courses/submissions.html',{'course':course,'submissions':submissions,
                                                     'submission_form':submission_form})

@login_required
def submit_assignment(request,course_id,assignment_id):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')
   elif request.user.is_tutor:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')
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
         submission.file_submission.delete()
         submission.delete()
         submit_form = SubmitForm()
         return render(request,'courses/submit_assignment.html',{'course':course,'assignments':assignments,
                                                           'assignment':assignment,'submit_form':submit_form})
   else:
      submit_form = SubmitForm()
   return render(request,'courses/submit_assignment.html',{'course':course,'assignments':assignments,
                                                           'assignment':assignment,'submit_form':submit_form})

@login_required
def view_tutor_course(request,course_id,post_id=None):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')
   elif request.user.is_student:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

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
            post_form = PostForm()
            material_form = MaterialForm()
            return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})
         else:
            print(post_form.errors)
            return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})

      elif 'delete_post_button' in request.POST:
         notice = get_object_or_404(Notice,pk=post_id)
         m1 = Material.objects.filter(notice=notice)
         if m1.exists() is True:
            m1 = m1[:1].get()
            m1.material.delete()
            m1.delete()
         notice.delete()
         notices = Notice.objects.filter(course=course)
         return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})

   return render(request,"courses/course.html",{'course':course,'notices':notices,
                                  'post_form':post_form,'material_form':material_form})

#For both tutors and students
@login_required
def view_questions_tutor(request,course_id,question_id=None,answer_id=None):

   if is_enrolled(request.user, course_id) is False:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

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
            question_form = QuestionForm()
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
         else:
            print(question_form.errors)
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})

      elif 'reply_button' in request.POST:
         answer_form = AnswerForm(data = request.POST)

         if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = get_object_or_404(Question,pk=question_id)
            answer.save()
            answer_form = AnswerForm()
            messages.success(request,'Answer successfully uploaded!')
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
         else:
            print(answer_form.errors)
            messages.error(request,"Error posting the answer!")
            return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})

      elif 'delete_question_button' in request.POST:
         question = get_object_or_404(Question,pk=question_id)
         question.delete()
         questions = Question.objects.filter(course=course)
         messages.success(request,'Question successfully deleted!')
         return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})
      elif 'delete_answer_button' in request.POST:
         answer = get_object_or_404(Answer,pk=answer_id)
         answer.delete()
         messages.success(request,'Answer successfully deleted!')
         return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                  'question_form':question_form,'answer_form':answer_form})

   return render(request,"courses/questions.html",{'course':course,'questions':questions,
                                                      'question_form':question_form,'answer_form':answer_form})

def is_enrolled(user, course_id):
   course = get_object_or_404(Course,pk=course_id)

   if user.is_tutor:
      tutor_courses = TutorCourse.objects.filter(course=course,tutor=user.Tutor)

      return tutor_courses.exists()
   else:
      student_courses = StudentCourse.objects.filter(course=course,student=user.Student)

      return student_courses.exists()
      

@login_required
def view_course(request,course_id,question_id=None):

   if request.user.is_tutor:
      return HttpResponse('<html><body><h2 style="font-weight: lighter">Your do not have access to view this page!</h2><body></html>')

   course = get_object_or_404(Course,pk=course_id)

   if request.method=='POST':
      if 'enroll_button' in request.POST:
         if (course.student_number + 1) > course.max_students:
            messages.warning(request,"There is no study places left!")
            tutors = Tutor.objects.filter(course=course)
            return render(request,"courses/enroll.html",{'course':course,'tutors':tutors})
         else:
            student_course = StudentCourse.objects.create(course=course,student=request.user.Student)
            course.student_number = course.student_number+1
            student_course.save()
            course.save()
            notices = Notice.objects.filter(course=course)
            messages.success(request,'Successfully enrolled!')
            return render(request,"courses/course.html",{'course':course,'notices':notices})

   student_courses = StudentCourse.objects.filter(course = course,student = request.user.Student) 
   if student_courses.exists() is False:
      tutors = Tutor.objects.filter(course=course)
      return render(request,"courses/enroll.html",{'course':course,'tutors':tutors})

   notices = Notice.objects.filter(course=course)

   return render(request,"courses/course.html",{'course':course,'notices':notices})