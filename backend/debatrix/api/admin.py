from django.contrib import admin
from .models import Debate, Comment, Percentage, ChatBot

class DebateModelAdmin(admin.ModelAdmin):
    list_display = ('debateId', 'creatorUserName', 'title', 'percentage', 'numOfPercentages', 'numberComments', 'created_at')
    exclude = ('likes','debateId',)
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user', 'parent_debate', 'date', 'content')
    
class PercentageAdmin(admin.ModelAdmin):
    list_display = ('user', 'debate', 'percentage')


# Here we must register the table Debates to be able to add debates as an admin as well as delete them. 
admin.site.register(Debate, DebateModelAdmin)
admin.site.register(Comment)
admin.site.register(Percentage, PercentageAdmin)
admin.site.register(ChatBot)