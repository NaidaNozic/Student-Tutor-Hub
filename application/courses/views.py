from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from courses.forms import NewUserForm, StudentProfileForm
from django.shortcuts import redirect

# Create your views here.

def register_student(request):
   if request.method=="POST":
      user_form = NewUserForm(data = request.POST)
      student_form = StudentProfileForm(data = request.POST)

      if user_form.is_valid() and student_form.is_valid():

         user = user_form.save()
         user.is_student = True
         user.save()
         #login(request, user)
			#messages.success(request,"Registration successful!")
         student = student_form.save(commit=False)
         student.user=user
         student.save()
         return redirect('../../../')

      else:
         print(user_form.errors,student_form.errors)
   else:
      user_form = NewUserForm()
      student_form = StudentProfileForm()

   return render(request,'authenticate/register_student.html',{'user_form':user_form,'student_form':student_form})