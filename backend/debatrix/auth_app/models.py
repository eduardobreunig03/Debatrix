from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#table for a user profile picture
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the User model (username or ID)
    profile_picture = models.ImageField(null = True, blank = True, upload_to = "images/")  #will be in  the media folder
    profile_bio = models.TextField(null = True, blank = True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

