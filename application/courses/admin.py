from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser,Student,Tutor,Course,TutorCourse,StudentCourse,Notice,Material,Question,Answer,Assignment,Submission

# Register your models here.

#class CustomUserAdmin(UserAdmin):
  #  fieldsets=(
     #   *UserAdmin.fieldsets,
      #  (
        #    'Additional Info',
         #   {
               # 'fields':(
                 #   'is_student',
                   # 'is_tutor'
 #               )
 #           }
 #       )
 #   )
fields=list(UserAdmin.fieldsets)
fields[1]=('Personal Info',{'fields':('first_name','last_name','email','is_student','is_tutor')})
UserAdmin.fieldsets=tuple(fields)

admin.site.register(NewUser, UserAdmin)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(TutorCourse)
admin.site.register(StudentCourse)
admin.site.register(Notice)
admin.site.register(Material)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Assignment)
admin.site.register(Submission)