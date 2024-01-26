from django.db import models

class DegreeProgram(models.Model):
    DegreeProgramID = models.AutoField(primary_key=True)
    DegreeProgramName = models.CharField(max_length=255)

    def __str__(self):
        return self.DegreeProgramName
    
class Teacher(models.Model):
    TeacherID = models.AutoField(primary_key=True)
    TeacherName = models.CharField(max_length=255)
    Education = models.CharField(max_length=255)
    ContactNumber = models.CharField(max_length=20)
    Description = models.TextField()

    def __str__(self):
        return self.TeacherName

class Course(models.Model):
    CourseID = models.AutoField(primary_key=True)
    DegreeProgramID = models.ForeignKey(DegreeProgram, on_delete=models.CASCADE)
    CourseName = models.CharField(max_length=255)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return self.CourseName

class Student(models.Model):
    StudentID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)  # In a real-world scenario, use a more secure method for storing passwords
    Email = models.EmailField()
    DegreeProgramID = models.ForeignKey(DegreeProgram, on_delete=models.CASCADE)

    def __str__(self):
        return self.Username

class Question(models.Model):
    DifficultyLevelChoices = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Difficult', 'Difficult'),
    ]

    QuestionID = models.AutoField(primary_key=True)
    QuestionText = models.TextField()
    Option1 = models.CharField(max_length=255)
    Option2 = models.CharField(max_length=255)
    Option3 = models.CharField(max_length=255)
    Option4 = models.CharField(max_length=255)
    CorrectOption = models.CharField(max_length=255)
    DifficultyLevel = models.CharField(max_length=10, choices=DifficultyLevelChoices)
    Weightage = models.IntegerField()
    CourseID = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.QuestionText


    
# models.py
class PaperSubmission(models.Model):
    SubmissionID = models.AutoField(primary_key=True)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE)
    DifficultyLevel = models.CharField(max_length=10, choices=Question.DifficultyLevelChoices)
    File = models.FileField(upload_to='paper_submissions/')
    StatusChoices = [
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Marked', 'Marked'),  # Added 'Marked' status
    ]
    Status = models.CharField(max_length=10, choices=StatusChoices, default='Submitted')
    Marks = models.IntegerField(blank=True, null=True)
    Grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f'{self.Student.Username} - {self.Course.CourseName} - {self.DifficultyLevel}'
