# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import DegreeProgram, Course, Question, Student, PaperSubmission , Teacher

admin.site.register(Teacher)

@admin.register(DegreeProgram)
class DegreeProgramAdmin(admin.ModelAdmin):
    list_display = ['DegreeProgramID', 'DegreeProgramName']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['CourseID', 'DegreeProgramID', 'CourseName']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['QuestionID', 'QuestionText', 'DifficultyLevel', 'Weightage', 'CourseID']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['StudentID', 'Username', 'Email', 'DegreeProgramID']

@admin.register(PaperSubmission)
class PaperSubmissionAdmin(admin.ModelAdmin):
    list_display = ['SubmissionID', 'Student', 'Course', 'DifficultyLevel', 'Status', 'Marks', 'Grade', 'file_download']

    def file_download(self, obj):
        file_url = obj.File.url
        return format_html('<a class="button" href="{}" download>Download File: {}</a>', file_url, file_url)

    file_download.short_description = 'Download File'

    actions = ['approve_paper', 'reject_paper']

    def approve_paper(self, request, queryset):
        queryset.update(Status='Approved')

    def reject_paper(self, request, queryset):
        queryset.update(Status='Rejected', Marks=None, Grade=None)

    approve_paper.short_description = 'Approve selected papers'
    reject_paper.short_description = 'Reject selected papers'
