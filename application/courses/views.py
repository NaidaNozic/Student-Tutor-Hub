from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from courses.forms import NewUserForm
from django.shortcuts import redirect

# Create your views here.

def register_student(request):
   if request.method=="POST":
      user_form = NewUserForm(data = request.POST)

      if user_form.is_valid():

         user = user_form.save()
         user.is_student = True
         user.save()
         #login(request, user)
			#messages.success(request,"Registration successful!")
         return redirect('../../../')

      else:
         print(user_form.errors)
   else:
      user_form = NewUserForm()

   return render(request,'authenticate/register_student.html',{'user_form':user_form,})