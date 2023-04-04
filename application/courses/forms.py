from django import forms
from django.contrib.auth.forms import UserCreationForm
from courses.models import NewUser,Student,Question,Answer,Submission,Notice,Material,Assignment
from django.db import transaction
from django.core.validators import MaxValueValidator, MinValueValidator

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

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label='First name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=False, label='Last name:', widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=False, label='Email:', widget=forms.EmailInput(attrs={"placeholder": "etc. name@example.com",
                                                                            "class":"form-control"}))
    class Meta():
        model = NewUser
        fields = ['first_name','last_name','email']


class StudentProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Phone number:', widget=forms.NumberInput(
        attrs={"placeholder": "etc. 38762878785","class":"form-control"}))
    age = forms.IntegerField(label='Age:', widget=forms.NumberInput(
        attrs={"max":999,"class":"form-control"}))

    class Meta():
        model =  Student
        fields = ['phone','age']

class MaterialForm(forms.ModelForm):
    material = forms.FileField(required=False)
    class Meta():
        model = Material
        fields = ['material']

class QuestionForm(forms.ModelForm):
    title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(label='Question:', 
                           widget=forms.Textarea(attrs={"rows":2,"cols":60,
                                                        "placeholder":"What is your question?",
                                                        "class":"form-control",
                                                        "id":"id_text1"}))

    class Meta():
        model =  Question
        fields = ['title','text']

class AnswerForm(forms.ModelForm):
    text = forms.CharField(label='Text:', widget=forms.Textarea(attrs={ "rows":5,"cols":60,
                                                                        "class":"form-control",
                                                                        "id":"id_text2"}))

    class Meta():
        model = Answer
        fields = ['text']

class PostForm(forms.ModelForm):
    name = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(label='Text:', widget=forms.Textarea(attrs={ "rows":2,"cols":60,
                                                                        "class":"form-control",
                                                                        "id":"id_text2"}))
    class Meta():
        model = Notice
        fields = ['name','text']

class SubmitForm(forms.ModelForm):
    file_submission = forms.FileField()
    class Meta():
        model = Submission
        fields = ['file_submission']
        
class UpdateSubmissionForm(forms.ModelForm):
    grade = forms.IntegerField(required=False,validators=[MaxValueValidator(100),MinValueValidator(1)],
                               widget=forms.NumberInput(attrs={'style': 'width:7ch'}))
    class Meta():
        model = Submission
        fields = ['grade']

class AssignmentForm(forms.ModelForm):
    name = forms.CharField(label='Assignment title:', widget=forms.TextInput(attrs={'class':'form-control'}))
    file_assignment = forms.FileField()
    class Meta():
        model = Assignment
        fields = ['name','file_assignment']
