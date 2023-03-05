from django import forms
from django.contrib.auth.forms import UserCreationForm
from courses.models import NewUser,Student

# Create your forms here.

## Register User Form
class NewUserForm(UserCreationForm):
    first_name = forms.CharField(label='First name:', widget=forms.TextInput(attrs={"placeholder": "Your first name..."}))
    last_name = forms.CharField(label='Last name:', widget=forms.TextInput(attrs={"placeholder": "Your last name..."}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={"placeholder": "Your username..."}))
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={"placeholder": "Your email..."}))
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password:', widget=forms.PasswordInput())

    class Meta():
        model = NewUser
        fields = ['first_name','last_name','username','email','password1','password2']

class StudentProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Phone number:', widget=forms.NumberInput(
        attrs={"placeholder": "Your phone (etc. 38762878785) :"}))
    age = forms.IntegerField(label='Age:', widget=forms.NumberInput(
        attrs={"placeholder": "Your age:", "max":999}))

    class Meta():
        model =  Student
        fields = ['phone','age']

