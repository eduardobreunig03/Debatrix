from rest_framework import generics
from .models import Debate, Comment , PinnedDebates, Percentage, ChatBot
from .serializers import DebateSerializer, CommentSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView
from django.http import JsonResponse
from .llm import llm_utils
from rest_framework.decorators import api_view
from .models import Percentage
from .serializers import PercentageSerializer
from .serializers import ChatBotSerializer
from rest_framework.permissions import IsAuthenticated
import json
from django.db.models import Avg
import random as rand

# Return all debates
class DebateAPIView(generics.ListAPIView):
    serializer_class = DebateSerializer

    def get_queryset(self):
        for debate in Debate.objects.all():
            debate.get_comment_count()
            debate.save()
        queryset = Debate.objects.all()  # Start with all debates
        search_query = self.request.query_params.get('search', None)
        sorted = self.request.query_params.get('trending',None)


        if search_query:
            # Filter the queryset to include debates with title or content containing the search query
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )
        if sorted:
            print("sorted")
            queryset = queryset.order_by('-numberComments')


        return queryset

# Called when a debate is saved
class SaveDebateView(APIView):
    def post(self, request):
        print("DATA", request.data)
        serializer = DebateSerializer(data=request.data)
        if serializer.is_valid():
            debate = serializer.save()
            return Response(DebateSerializer(debate).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['DELETE'])
def delete_debate(request, debate_id):
    try:
        debate = Debate.objects.get(debateId=debate_id)
        debate.delete()
        return Response({"message": "Debate deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Debate.DoesNotExist:
        return Response({"error": "Debate not found"}, status=status.HTTP_404_NOT_FOUND)


class CommentAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        debate_id = self.request.query_params.get("debateId", None)
        if debate_id:
            return Comment.objects.filter(parent_debate__debateId=debate_id)
      
       
        return Comment.objects.all()

    def create(self, request, *args, **kwargs):
        # print(Debate.objects.get(request.data.get("parent_debate")))
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            debate_id = request.data.get('parent_debate')
            debate = Debate.objects.get(debateId=debate_id)
            debate.get_comment_count()
            debate.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Detailed error response
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# For AI model -> generate summary
class RunLLMView(APIView):
    def post(self, request):
        def handle_summarise():
            output = llm_utils.summarise(input_text)
            # try:
            #     output.split("\n")
            # except:
            #     output = "error summarising"

            return output
        
        def handle_fact_check():
            return llm_utils.fact_check(input_text)
        
        action = request.data.get('action', '')
        input_text = request.data.get('input_text', '')
        
        if not input_text:
            return JsonResponse({'error': 'No input text provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        if action == 'summarise':
            output = handle_summarise()
        elif action == 'factcheck':
            output = handle_fact_check()
        else:
            return JsonResponse({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        return JsonResponse({'output': output}, status=status.HTTP_200_OK)
    
class GetPercentageView(APIView):
    def get(self, request):
        debate_id = request.query_params.get('debateId')
        username = request.query_params.get('user')

        try:
            debate = Debate.objects.get(debateId=debate_id)
            percentage = Percentage.objects.get(debate=debate, user=username)

            return Response({'percentage': percentage.percentage}, status=status.HTTP_200_OK)

        except Percentage.DoesNotExist:
            return Response({'percentage': 50}, status=status.HTTP_200_OK)

        except Debate.DoesNotExist:
            return Response({'error': 'Debate not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddPercentageView(APIView):
    """
    This view handles the creation or updating of a percentage for a user in a specific debate.
    """

    def post(self, request):
       
        debate_id = request.data.get('debateId')
        percentage_value = request.data.get('percentage')
        username = request.data.get('user')  

        print("debate_id", debate_id)
        print("percentage_value", percentage_value)
        print("username", username)


       
        if not all([debate_id, percentage_value, username]):
            return Response({"error": "Missing data. Debate ID, percentage, and username are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            debate = Debate.objects.get(debateId=debate_id)
            
            percentage_obj, created = Percentage.objects.update_or_create(
                user=username,  
                debate=debate,
                defaults={'percentage': percentage_value}
            )
            print(created)
            print("Printiong after saving percentage")

            if created:
                print("Percentage created successfully")
                return Response({"message": "Percentage created successfully"}, status=status.HTTP_201_CREATED)
            else:
                print("Percentage updated successfully")
                return Response({"message": "Percentage updated successfully"}, status=status.HTTP_200_OK)

        except Debate.DoesNotExist:
            return Response({"error": "Debate not found"}, status=status.HTTP_404_NOT_FOUND)

        

# Save pinned debates
class SavePinnedDebatesView(APIView):
    permission_classes = [IsAuthenticated]
    print("SavePinnedDebatesView")
    def post(self, request):
        debate_id = request.data.get('debateId', None)
        user = request.user
        
        if not debate_id:
            return JsonResponse({'error': 'No post_id provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        debate = Debate.objects.get(debateId=debate_id)
        pinned_debate = PinnedDebates.objects.create(debate=debate, user=user)
        
        return JsonResponse({'message': f'{user.username} pinned {debate.title}'}, status=status.HTTP_201_CREATED)

# Get pinned debates for a user
class GetPinnedDebatesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        # Fetch the debates related to the pinned debates
        pinned_debates = PinnedDebates.objects.filter(user=user).select_related('debate')
        debates = [pinned_debate.debate for pinned_debate in pinned_debates]

        # Serialize the debate objects
        serializer = DebateSerializer(debates, many=True)
        
        return Response(serializer.data)

class UnpinDebateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        debate_id = request.data.get('debateId', None)
        user = request.user
        
        if not debate_id:
            return JsonResponse({'error': 'No debateId provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Use filter() to get all matching pinned debates for this user and debate
            pinned_debates = PinnedDebates.objects.filter(debate__debateId=debate_id, user=user)
            
            if pinned_debates.exists():
                # Delete all pinned debates found
                pinned_debates.delete()
                return JsonResponse({'message': f'Debate {debate_id} unpinned successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Pinned debate not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class AveragePercentageView(APIView):
    def get(self, request, debate_id):
        try:
            
            debate = Debate.objects.get(debateId=debate_id)
            
            
            average_percentage = Percentage.objects.filter(debate=debate).aggregate(Avg('percentage'))['percentage__avg']
        
            if average_percentage is None:
                average_percentage = 0
            
            return Response({"average_percentage": average_percentage}, status=status.HTTP_200_OK)
        
        except Debate.DoesNotExist:
            return Response({"error": "Debate not found"}, status=status.HTTP_404_NOT_FOUND)
        
class GetBotComment(APIView):
    def get(self, request):
        # Check if any ChatBot objects exist
        count = ChatBot.objects.count()
        if count == 0:
            return Response({"error": "No bots found in the database"}, status=status.HTTP_404_NOT_FOUND)

        # Get a random ChatBot instance
        bot = ChatBot.objects.all()[rand.randint(0, count - 1)]

        # Retrieve the content from the request (assuming GET params are used)
        prompt = request.query_params.get('content', '')

        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the LLM response using the bot's name and the prompt
            content = llm_utils.get_llm_response(bot.name, prompt)
            return Response({
                "bot_comment": content,
                "username": bot.user.username
                }, status=status.HTTP_200_OK)
        except Exception as e:
            # In case the LLM utility function throws an error
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
