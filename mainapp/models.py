from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15,unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    adress=models.CharField(max_length=20,null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Title = models.CharField(max_length=200)
    Text = models.TextField()
    vaqti = models.DateTimeField(auto_now_add=True) 
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.Title}"