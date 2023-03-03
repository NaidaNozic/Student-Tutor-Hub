from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class NewUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(NewUser,on_delete=models.CASCADE,primary_key=True,related_name='Student')
    phone = models.IntegerField()
    age = models.IntegerField(null=True,blank=True) #this field is optional

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name
