from django.db import models
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectField
from datetime import datetime    
from django.utils.timezone import now
# Create your models here.

class Article(models.Model):
  categoryList = [
    ('basic_robotics', 'Basic Robotics'),
    ('advanced_robotics', 'Advanced Robotics'),
    ('soft_robotics', 'Soft Robotics'),
    ('medical_robotics', 'Medical Robotics'),
    ('cad', 'CAD'),
    ('simulation', 'Simulation'),
    ('machine_learning', 'Machine Learning'),
    ('deep_learning', 'Deep Learning'),
    ('image_processing', 'Image Processing'),
    ('generative_ai', 'Generative AI'),
    ('intelligent_system', 'Intelligent System'),
    ('tensorflow', 'Tensoflow'),
    ('pytorch', 'Pytorch'),
    ]
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='articles')
  title = models.CharField(max_length = 200)
  desc = models.CharField(max_length = 200)
  artImage = models.ImageField(upload_to = 'art_photos', default = './images/default.jpg', null = True, blank = True)
  content = models.TextField()
  category = MultiSelectField(choices=categoryList,  max_choices=3)
  created = models.DateTimeField(default=now, editable=False) 
  bookmarks = models.ManyToManyField(get_user_model(), related_name='bookmarks')
  upvote = models.ManyToManyField(get_user_model(), related_name='up')
  downvote = models.ManyToManyField(get_user_model(), related_name='down')
  
  class Meta:
    ordering = ['-created']
  def  __str__(self):
    return f'{self.owner} writes an article at {self.created}'
  
class Comment(models.Model):
  owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='owner')
  article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name = 'article')
  created = models.DateTimeField(default=now, editable=False)
  content = models.TextField(max_length = 200)
  class Meta:
    ordering = ['-created']
  def __str__(self):
    return f"{self.owner} write a comment at {self.created}"