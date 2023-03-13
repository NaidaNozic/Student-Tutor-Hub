from django import forms
from django.contrib.auth.forms import UserCreationForm
from courses.models import NewUser,Student,Question,Answer

# Create your forms here.

## Register User Form
class NewUserForm(UserCreationForm):
    first_name = forms.CharField(label='First name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(label='Username:', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email:', widget=forms.EmailInput(attrs={"placeholder": "etc. name@example.com",
                                                                            "class":"form-control"}))
    password1 = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label='Repeat password:', widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta():
        model = NewUser
        fields = ['first_name','last_name','username','email','password1','password2']

class StudentProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Phone number:', widget=forms.NumberInput(
        attrs={"placeholder": "etc. 38762878785","class":"form-control"}))
    age = forms.IntegerField(label='Age:', widget=forms.NumberInput(
        attrs={"max":999,"class":"form-control"}))

    class Meta():
        model =  Student
        fields = ['phone','age']

class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(label='Question:', 
                           widget=forms.Textarea(attrs={"rows":2,"cols":60,
                                                        "placeholder":"What is your question?",
                                                        "class":"form-control"}))

    class Meta():
        model =  Question
        fields = ['title','text']

class AnswerForm(forms.ModelForm):
    text = forms.CharField(label='Text:', widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta():
        model = Answer
        fields = ['text']
