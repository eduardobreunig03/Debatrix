from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import random as rand

from auth_app.models import UserProfile
from .llm import llm_utils

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

# Debate table that containts all the information we need 
class Debate(models.Model):
    debateId = models.IntegerField()
    creatorUserName = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000) 
    created_at = models.DateTimeField(auto_now_add=True)
    percentage = models.IntegerField(default=0)
    numberComments = models.IntegerField(default=0)
    numOfPercentages = models.IntegerField(default=0)


    # Here we are saying if we want to print this object, we print the title of the debate. 
    def __str__(self):
        return self.title
    
    # Here is some custom code for when you save something in the debates.
    def save(self, *args, **kwargs):
        # Handling logic regarding debate ID and it increments one from the max and saves it automatically. 
        if not self.debateId:
            max_id = Debate.objects.aggregate(max_id=models.Max('debateId'))['max_id']
            if max_id is None:
                next_id = 1
            else:
                next_id = int(max_id) + 1
            self.debateId = next_id

        super().save(*args, **kwargs)
    

    def get_comment_count(self):
        numberComments = 0
        for comment in Comment.objects.all():
            if comment.parent_debate == self:
                numberComments+=1

        self.numberComments = numberComments


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    parent_debate = models.ForeignKey(Debate, related_name='api_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # Allow null and blank
    username = models.TextField(null=True, blank=True)
    profilepicture = models.TextField(null=True, blank=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='api_replies')
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    num_likes = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"}: {self.content[:30]}'
    

class Percentage(models.Model):
    user = models.CharField(max_length=150, default="Anonymous") 
    debate = models.ForeignKey(Debate, related_name="percentages", on_delete=models.CASCADE, null=True)
    percentage = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'debate') 
    
    def __str__(self):
        return f"{self.user}: {self.percentage}% on {self.debate.title}"

class PinnedDebates(models.Model):
    debate = models.ForeignKey(Debate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} pinned {self.debate.title}'

    
class ChatBot(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # Allow null and blank
    bot_id = models.IntegerField()
    name = models.CharField(max_length=100)
    modelfile = models.TextField()

    @classmethod
    def create_chatbot(cls, bot_id, name, modelfile):
        # Create the LLM model (assuming this function does the necessary setup)
        llm_utils.create_llm_model(name, modelfile)

        # Create or get a user associated with this ChatBot
        user, created = User.objects.get_or_create(
            username="AI " + name,
            defaults={
                'email': 'default@default.com',
                'password': 'chatbot_password',  # Set a default password (consider hashing in real applications)
            }
        )

        # Create a user profile for the chatbot user if it doesn't exist
        UserProfile.objects.get_or_create(user=user)
        
        # Create the ChatBot instance and return it
        chatbot = cls.objects.create(user=user, bot_id=bot_id, name=name, modelfile=modelfile)
        return chatbot

    def create_llm_for_chatbot(self):
        llm_utils.create_llm_model(self.name, self.modelfile)

    def create_user_for_chatbot(self):
        user, created = User.objects.get_or_create(
            username="AI " + self.name, 
            defaults={
                'email': 'default@default.com',
                'password': 'chatbot_password',
            }
        )
        UserProfile.objects.get_or_create(user=user)
        self.user = user
        self.save()
        return user
