from django.db import models
from django.contrib.auth.models import User
import os

# ------------------------
# SYSTEM ADMIN
# ------------------------

class SystemAdmin(models.Model):
    name = models.CharField(max_length=30, default="System Admin")
    number = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    address = models.TextField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# ------------------------
# COURSE (Financial Literacy)
# ------------------------

class Course(models.Model):

    category_choices = [
        ('finance','Financial Literacy'),
        ('saving','Saving & Budgeting'),
        ('banking','Banking & UPI'),
        ('loans','Loans & Credit'),
        ('insurance','Insurance'),
        ('fraud','Fraud Awareness'),
        ('investment','Simple Investments'),
        ('govt','Government Schemes')
    ]

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=category_choices)
    description = models.TextField(max_length=500)
    language = models.CharField(max_length=50, default="Hindi & English")
    is_active = models.BooleanField(default=True)
    image_url = models.ImageField(upload_to='courses/', default='courses/default.jpg', blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_course = Course.objects.get(pk=self.pk)
                if old_course.image_url != self.image_url:
                    if old_course.image_url.name != 'courses/default.jpg':
                        if os.path.exists(old_course.image_url.path):
                            os.remove(old_course.image_url.path)
            except Course.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.course_name


# ------------------------
# MODULES (Your 10 Finance Topics)
# ------------------------

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    order = models.IntegerField()

    def __str__(self):
        return self.title


# ------------------------
# VIDEO LESSONS
# ------------------------

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


# ------------------------
# STUDENT
# ------------------------

class Student(models.Model):
    name = models.CharField(max_length=30, default="Student")
    number = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True)
    address = models.TextField(max_length=100, blank=True)
    username = models.CharField(max_length=20, unique=True, default="student")
    password = models.CharField(max_length=50, blank=True)
    enrolled_courses = models.ManyToManyField(Course, related_name='students', blank=True)

    def __str__(self):
        return self.name


# ------------------------
# COURSE REQUEST
# ------------------------

class CourseRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_requests')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_requests')
    request_date = models.DateField(auto_now=True)
    reason = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=20, default="pending")

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student.name} request for {self.course.course_name}"


# ------------------------
# LESSON PROGRESS (Video Tracking)
# ------------------------

class LessonProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.name} - {self.lesson.title}"

