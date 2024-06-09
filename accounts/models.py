from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create a custom user model
class CustomUser(AbstractUser):
    
    DESIGNATION_CHOICE = (
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Lecturer', 'Lecturer'),
    )
    
    is_faculty = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True, null=True)
    university = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True, choices=DESIGNATION_CHOICE)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    research_activities = models.TextField(blank=True, null=True)
    membership = models.TextField(blank=True, null=True)
    publication = models.TextField(blank=True, null=True)
    award = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    scholar_link = models.CharField(max_length=100, blank=True, null=True)
    github_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics', default='./images/default.jpg', null=True, blank=True)
    