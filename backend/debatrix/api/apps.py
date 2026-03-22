from django.apps import AppConfig
from .llm import llm_utils

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'  # Ensure this matches the app directory name

    def ready(self):
        from .models import ChatBot, User
        from auth_app.models import UserProfile
        from django.db.utils import OperationalError
        
        llm_utils.create_llm_model(
            name='summarise', 
            modelfile='''
            FROM llama3.1
            PARAMETER temperature 0
            SYSTEM " 
                You will be given a text. Your job is to break down the text into points that summarise the text. 
                If the text is too small to summarise simply output nothing. 
                Output each new point on a new line.
                Do not output anything else apart from the summary of the text. Only output the summarised text.
                Do not announce that you are summarising the text.
            "
            '''
        )
        llm_utils.create_llm_model(
            name='factcheck',
            modelfile='''
            FROM llama3.1
            PARAMETER temperature 0
            SYSTEM "
            You will be given a text. 
            Your job is to break down the text into points that summarise the text and fact check each statment by outputting whether the statement is true, false or partially true, and then give a brief reason why. 
            Make sure that you only output the summarised points and the fact checking. 
            Do not explain what you are doing or output anything else.

            Output in the form of a list of brief summarised sentences that encapsulate each point in the text.
            For example: 'The earth is flat' This is FALSE because ...
            "
            '''
        )

        try:
            # create the llm model for each ai chatbot
            chatbots = ChatBot.objects.all()
            for chatbot in chatbots:
                chatbot.create_llm_for_chatbot()
                chatbot.create_user_for_chatbot()
                
        except OperationalError:
            print("Database is not ready yet (migrations might not be applied).")
