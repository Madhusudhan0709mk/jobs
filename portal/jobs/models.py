from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.user.username
    
class createjobposts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null = True)
    companyname = models.CharField(max_length=100)
    cgpa = models.CharField(max_length=255)  # Assuming it's a decimal field, change to FloatField
    skills = models.CharField(max_length=255)  # Set the maximum length
    address = models.CharField(max_length=255)  # Set the maximum length
    email = models.EmailField()
    about = models.CharField(max_length=400)
    created_at = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.companyname
    
class applyjob(models.Model):
    status_choices = (
        ('accepted','accepted'),
        ('declined','declined'),
        ('pending','pending')
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    createjobposts =models.ForeignKey(createjobposts,on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=status_choices)
    
    def __str__(self):
        return f'{self.user}+{self.createjobposts}'
    
    
