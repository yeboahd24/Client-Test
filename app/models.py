from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.enums import Choices

# Create your models here.
class User(AbstractUser):
    is_developer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Developer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
 
    
    def __str__(self):
        return self.user.first_name

class ProjectManager(models.Model):
    user = models.OneToOneField(User,models.CASCADE)
    
    def __str__(self):
        return self.user.first_name

class Ticket(models.Model):
    ticket_title = models.CharField(unique=True,max_length=200)
    ticket_description = models.TextField()
    created_by = models.ForeignKey(User,related_name = 'created_by',blank=True,null=True,on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('Opened','Opened'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Closed','Closed')
    )

    status = models.CharField('Status',choices=STATUS_CHOICES,max_length = 100,blank=True,null=True)

    closed_date = models.DateTimeField(blank=True,null=True)

    accepted_by = models.ForeignKey(User,related_name='assigned_to',on_delete=models.CASCADE,blank=True,null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.ticket_title
