# Generated by Django 4.1.7 on 2023-04-26 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0016_course_student_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=600),
        ),
    ]
