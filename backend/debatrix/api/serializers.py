from rest_framework import serializers
from .models import Debate 
from auth_app.models import UserProfile
from .models import Comment
from .models import Percentage
from .models import ChatBot

class PercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Percentage
        fields = ['user', 'debate', 'percentage']

    def create(self, validated_data):
        
        percentage_obj, created = Percentage.objects.update_or_create(
            user=validated_data.get('user'),
            debate=validated_data.get('debate'),
            defaults={'percentage': validated_data.get('percentage')}
        )
        return percentage_obj


class DebateSerializer(serializers.ModelSerializer):
    debateId = serializers.IntegerField(read_only=True)
    percentage = serializers.IntegerField(read_only=True)
    numberComments = serializers.IntegerField(read_only=True)
    creatorUserName = serializers.CharField()
    percentages = PercentageSerializer(many=True, read_only=True)

    class Meta:
        model = Debate
        fields = ['debateId', 'title', 'content', 'creatorUserName', 'created_at', 'percentage', 'numOfPercentages', 'numberComments', 'percentages']
        # extra_kwargs = {'creatorUserName': {'write_only': True}}

    def create(self, validated_data):
        # username = validated_data.pop('creatorUserName')
        print("Validated",validated_data)
        # user_profile = UserProfile.objects.get(user__username=username)
        # validated_data['userProfile'] = user_profile
        return super().create(validated_data)        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'parent_debate', 'user', 'username', 'profilepicture', 'parent_comment', 'date', 'content', 'num_likes', 'depth']
        read_only_fields = ['comment_id', 'date', 'num_likes', 'depth']

    def validate(self, data):
        print("validating")
        if data.get('parent_comment'):
            parent_comment = data['parent_comment']
            parent_debate = data['parent_debate']
            if parent_comment.parent_debate != parent_debate:
                raise serializers.ValidationError({
                    "parent_debate": "Parent comment must belong to the same debate."
                })
        return data

class ChatBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBot
        fields = '__all__'

