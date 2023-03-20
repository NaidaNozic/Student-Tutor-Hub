# Generated by Django 4.1.7 on 2023-03-20 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_assignment_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_name', to='courses.student'),
        ),
    ]
