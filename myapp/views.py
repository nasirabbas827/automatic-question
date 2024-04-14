# views.py
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student , Course
from .forms import StudentLoginForm
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm
from django.http import HttpResponse
from docx import Document
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Course, Question
from random import sample
from django.contrib.auth.decorators import login_required

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()

            # Store student information in session
            request.session['student_id'] = student.StudentID

            return redirect('student_dashboard')  # Redirect to the student dashboard
    else:
        form = StudentRegistrationForm()

    return render(request, 'register.html', {'form': form})


def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['Password']

            # In a real-world scenario, you would use a more secure authentication method
            student = Student.objects.filter(Username=username, Password=password).first()

            if student:
                # Store student information in session
                request.session['student_id'] = student.StudentID
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = StudentLoginForm()

    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect

def student_dashboard(request):
    # Check if a student is logged in (based on the presence of 'student_id' in the session)
    if 'student_id' not in request.session:
        # Redirect to the login page or handle the case when a student is not logged in
        return redirect('student_login')  # Replace 'student_login' with the actual URL name for your student login view

    # Retrieve student information from session
    student_id = request.session.get('student_id')
    student = Student.objects.get(pk=student_id)

    # Retrieve courses associated with the student's degree program
    courses = Course.objects.filter(DegreeProgramID=student.DegreeProgramID)

    return render(request, 'dashboard.html', {'student': student, 'courses': courses})


def course_details(request, course_id):
    # Retrieve student information from session
    student_id = request.session.get('student_id')
    student = Student.objects.get(pk=student_id)

    # Retrieve the selected course
    course = Course.objects.get(pk=course_id)

    return render(request, 'course_details.html', {'student': student, 'course': course})
from random import choices


def generate_paper(request, course_id, difficulty_level):
    # Retrieve the selected course
    course = Course.objects.get(pk=course_id)

    # Retrieve questions based on the selected difficulty level and course
    questions = Question.objects.filter(CourseID=course, DifficultyLevel=difficulty_level)

    # Ensure there are questions for the selected difficulty level
    if not questions.exists():
        messages.error(request, f'No questions available for the {difficulty_level} difficulty level.')
        return redirect('course_details', course_id=course_id)

    # Select random questions based on weightage to make a total of 100 marks
    selected_questions = choose_questions(questions)

    # Retrieve student information from session
    student_id = request.session.get('student_id')
    student = Student.objects.get(pk=student_id)

    # Pass options along with questions
    questions_with_options = [
        {'question': question, 'options': [question.Option1, question.Option2, question.Option3, question.Option4]}
        for question in selected_questions
    ]

    return render(request, 'generated_paper.html', {'course': course, 'difficulty_level': difficulty_level, 'questions': questions_with_options, 'student': student})


import random
from io import BytesIO
from docx import Document
from django.http import HttpResponse
from .models import Course, Question

def choose_questions(questions):
    # Create a list of question weights based on their weightage
    question_weights = [question.Weightage for question in questions]

    # Choose random questions based on their weightage until the total weight reaches 100
    selected_questions = []
    total_weight = 0
    while total_weight < 100:
        # Choose a question based on its weightage
        chosen_question = random.choices(questions, weights=question_weights, k=1)[0]

        # Add the chosen question to the list
        selected_questions.append(chosen_question)

        # Update the total weight
        total_weight += chosen_question.Weightage

    return selected_questions


def download_paper(request, course_id, difficulty_level):
    # Retrieve the selected course
    course = Course.objects.get(pk=course_id)

    # Retrieve questions based on the selected difficulty level and course
    questions = Question.objects.filter(CourseID=course, DifficultyLevel=difficulty_level)

    # Choose questions for the paper
    selected_questions = choose_questions(questions)

    # Create a Word document
    document = Document()
    document.add_heading(f'{course.CourseName} - {difficulty_level} Difficulty', level=1)

    # Add questions to the document
    for question in selected_questions:
        document.add_paragraph(question.QuestionText, style='Heading1')
        document.add_paragraph('Options:')
        for option in [question.Option1, question.Option2, question.Option3, question.Option4]:
            document.add_paragraph(f'- {option}')
        document.add_paragraph('')  # Add an empty line between questions

    # Save the document to a BytesIO buffer
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    # Create a response with the Word document
    response = HttpResponse(buffer.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = f'attachment; filename={course.CourseName}_{difficulty_level}_Paper.docx'

    return response


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Course, Question, PaperSubmission
from .forms import StudentRegistrationForm, StudentLoginForm


def submit_paper(request, course_id, difficulty_level):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        student = Student.objects.get(pk=student_id)
        course = Course.objects.get(pk=course_id)
        file = request.FILES['file']

        submission = PaperSubmission.objects.create(
            Student=student,
            Course=course,
            DifficultyLevel=difficulty_level,
            File=file,
            Status='Submitted'
        )

        messages.success(request, 'Paper submitted successfully.')
        return redirect('student_dashboard')

    return redirect('generate_paper', course_id=course_id, difficulty_level=difficulty_level)



from .models import PaperSubmission

def view_submitted_papers(request):
    # Check if a student is logged in (based on the presence of 'student_id' in the session)
    if 'student_id' not in request.session:
        # Redirect to the login page or handle the case when a student is not logged in
        return redirect('student_login')  # Replace 'student_login' with the actual URL name for your student login view

    # Retrieve the student's ID from the session
    student_id = request.session['student_id']

    # Retrieve the student from the database
    student = Student.objects.get(pk=student_id)

    # Filter PaperSubmission objects based on the logged-in student and 'Marked' status
    student_submissions = PaperSubmission.objects.filter(Student=student, Status='Marked')

    return render(request, 'view_submitted_papers.html', {'submissions': student_submissions, 'student': student})

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import PaperSubmission

def download_submitted_paper(request, submission_id):
    # Retrieve the submitted paper
    submission = get_object_or_404(PaperSubmission, SubmissionID=submission_id)


    # Get the file content
    file_content = submission.File.read()

    # Create a response with the file content
    response = HttpResponse(file_content, content_type='application/octet-stream')
    
    # Set the Content-Disposition header to trigger download
    response['Content-Disposition'] = f'attachment; filename={submission.File.name}'

    return response



from django.shortcuts import render
from .models import Notification

def view_notifications(request):
    # Get all notifications for the current user
    notifications = Notification.objects.all()

    # Pass the notifications to the template
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_view(request):
    # Use Django's logout function to log the user out
    logout(request)
    return redirect('student_login')  # Replace 'student_login' with the actual URL name for your login view

