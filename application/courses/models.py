from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class NewUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

class Course(models.Model):
    name = models.CharField(max_length=250)
    summary = models.CharField(max_length=500)
    image = models.ImageField(upload_to="courses_images",default="courses_images/default.jpg",blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(NewUser,on_delete=models.CASCADE,primary_key=True,related_name='Student')
    phone = models.IntegerField()
    age = models.IntegerField(null=True,blank=True) #this field is optional
    course = models.ManyToManyField(Course,through="StudentCourse")

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class Tutor(models.Model):
    user = models.OneToOneField(NewUser,on_delete=models.CASCADE,primary_key=True,related_name='Tutor')
    phone = models.IntegerField()
    course = models.ManyToManyField(Course,through="TutorCourse")

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name

class StudentCourse(models.Model):
    course = models.ForeignKey(Course,related_name="course_name_student",on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name="student_name",on_delete=models.CASCADE)

    def __str__(self):
        return self.student.user.username+' '+self.course.name

    class Meta:
        unique_together = ('course','student')

class TutorCourse(models.Model):
    course = models.ForeignKey(Course,related_name="course_name_tutor",on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor,related_name="tutor_name",on_delete=models.CASCADE)

    def __str__(self):
        return self.tutor.user.username+' '+self.course.name

    class Meta:
        unique_together = ('course','tutor')

class Notice(models.Model):
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=500,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    tutor = models.ForeignKey(Tutor,related_name='tutor_upload',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='course_notice',on_delete=models.CASCADE)

    def __str__(self):
        return 'Notice: '+self.name

class Material(models.Model):
    notice = models.ForeignKey(Notice,related_name='material_notice',on_delete=models.CASCADE)
    material = models.FileField(upload_to='materials')

    def __str__(self):
        return str(self.material)

class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course,related_name='course_question',on_delete=models.CASCADE)
    student = models.ForeignKey(Student,related_name='student_question',on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(NewUser,related_name='user_answer',on_delete=models.CASCADE)
    question = models.ForeignKey(Question,related_name='answer_question',on_delete=models.CASCADE)
    text = models.CharField(max_length=550)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Reply from '+self.user.username

class Assignment(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course,related_name='course_assignment',on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor,related_name='tutor_assignment',on_delete=models.CASCADE)
    file_assignment = models.FileField(upload_to='assignments')

    def __str__(self):
        return 'Assignment: '+self.name

    class Meta:
        ordering = ['-created_at']

class Submission(models.Model):
    student = models.ForeignKey(Student,related_name='student_submission',on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment,related_name='assignment_submission',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    file_submission = models.FileField(upload_to='submissions')

    def __str__(self):
        return 'Submitted '+self.assignment.name+' by '+self.student.user.username

    def delete(self, *args, **kwargs):
        self.file_submission.delete()
        super().delete(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']