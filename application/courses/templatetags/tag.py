from django import template
from ..models import Material,Answer,Assignment,Submission,Student,Tutor
from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def getMaterials(notice):
    
    materials = Material.objects.filter(notice=notice)
    
    return materials

@register.simple_tag
def getAnswers(question):

    answers = Answer.objects.filter(question=question)
    
    return answers

@register.simple_tag
def getAssignments(course):

    assignments = Assignment.objects.filter(course=course)

    return assignments

@register.simple_tag
def getSubmissionsByUser(user):

    student = get_object_or_404(Student,user=user)
    submissions = Submission.objects.filter(student=student)

    return submissions

@register.simple_tag
def getAssignmentsBySubmissions(submissions):

    assignment_list = [x.assignment for x in submissions]

    return assignment_list

@register.filter
def getGrade(list, assignment):

    for s in list:
        if s.assignment.pk is assignment.pk:
            if s.grade is None:
                return 'Not graded'
            else:
                return s.grade

    return 'Not graded'

@register.simple_tag
def getStudent(user):

    student = get_object_or_404(Student,user=user)
    return student

@register.simple_tag
def getTutor(user):

    tutor = get_object_or_404(Tutor,user=user)
    return tutor

@register.simple_tag
def getSubmittedAssignments(user):

    student = get_object_or_404(Student,user=user)
    submission_list = Submission.objects.filter(student=student)
    submissions = [x.assignment for x in submission_list]

    return submissions

@register.simple_tag
def getTutorsOfCourse(course):
    tutors = Tutor.objects.filter(course=course)
    return tutors