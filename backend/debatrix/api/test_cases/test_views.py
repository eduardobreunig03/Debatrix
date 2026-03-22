from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Debate, Comment, Percentage, ChatBot, PinnedDebates
from django.contrib.auth.models import User
from ..views import RunLLMView
from rest_framework_simplejwt.tokens import RefreshToken

# TESTING DEBATES #
class DebateTests(APITestCase):


    def setUp(self):
        # SETTING UP ENVIRONMENT WITH USER AND DEBATES AND LOGGING IN
        self.user = User.objects.create_user(username="testuser", password="password")
        self.debate = Debate.objects.create(title="Test Debate", content="This is a test debate.")
        self.client.login(username="testuser", password="password")



    def test_get_all_debates(self):
        # SIMPLE TEST TO GET ALL DEBATES
        url = reverse("debates")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # checking if the API returns the correct status code
        self.assertIn("title", response.data[0]) # checking if the API returns the correct content



    def test_get_all_debates_unauthenticated(self):
        # EDGE CASE: TEST TO GET ALL DEBATES WHEN UNAUTHENTICATED 
        response = self.client.get(reverse("debates"))  
        self.assertEqual(response.status_code, status.HTTP_200_OK) # expecting the same thing for both authorised/unauthorised 




    def test_save_debate(self):
        # SIMPLE TEST TO SAVE DEBATE WITH CONTENT 
        url = reverse("save_debate")  # Updated to match your urlpatterns
        data = {
            "title": "New Debate",
            "content": "Content of new debate",
            "creatorUserName": self.user.username  # Add the creator's username
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Debate")
    
    def test_save_debate_missing_fields(self):
        # EDGE CASE: SAVE DEBATE WITH MISSING FIELDS 
        url = reverse("save_debate")
        data = {
            "title": "New Debate",
            "creatorUserName": self.user.username
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    # EDGE CASE: SAVING DEBATE WITH UNAUTHORISED USER (not needed because button is missing and unable to be accessed by user)


    def test_delete_debate(self):
        # SIMPLE TEST TO DELETE DEBATE 
        url = reverse("delete_debate", kwargs={"debate_id": self.debate.debateId})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_debate_not_found(self):
        # EDGE CASE: DELETEING A DEBATE THAT DOESN'T EXIST 
        url = reverse("delete_debate", kwargs={"debate_id": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# TESTING COMMENTING #
class CommentTests(APITestCase):

    def setUp(self):
        # CREATES SAMPLE DEBATE TO TEST COMMENTS ON 
        self.debate = Debate.objects.create(title="Debate with Comments", content="Content here")
    
    def test_create_comment(self):
        # TESTS THAT A USER IS ABLE TO CREATE A COMMENT ON THE DEBATE
        url = reverse("comments") 
        data = {"content": "This is a comment", "parent_debate": self.debate.debateId}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "This is a comment")

    def test_create_comment_missing_fields(self):
        # EDGE CASE: TEST THAT A REQUEST TO CREATE A COMMENT WITH MISSING FIELDS FAILS
        url = reverse("comments")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RunLLMViewTests(APITestCase):

    def setUp(self):
        # SET UP URL FOR RUNNING LLM ACTIONS
        self.url = reverse("run_llm")  # Updated to match your urlpatterns

    def test_summarise_action(self):
        # TESTS THAT THE AI IS ABLE TO SUMMARISE GIVEN INPUT
        data = {"action": "summarise", "input_text": "This is a long text to summarise."}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()  # Use response.json() here
        self.assertIn("output", response_data)

    def test_run_llm_fact_check(self):
        # TESTS THAT THE AI IS ABLE TO FACT CHECK GIVEN INPUT
        data = {
            'action': 'factcheck',
            'input_text': 'This is a test input text for fact-checking.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()  # Change this line
        self.assertIn('output', response_data)  # Check if 'output' is in response

    def test_run_llm_no_input_text(self):
        # EDGE CASE: TEST THE CASE WHEN NO INPUT TEXT IS PROVIDED
        data = {
            'action': 'summarise'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()  # Change this line
        self.assertIn('error', response_data)  # Check if 'error' is in response

    def test_run_llm_invalid_action(self):
        # EDGE CASE: TEST THE CASE WHEN AN INVALID ACTION IS PROVIDED
        data = {
            'action': 'invalid_action',
            'input_text': 'This input text is for an invalid action.'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.json()  # Change this line
        self.assertIn('error', response_data)  # Check if 'error' is in response


class PercentageTests(APITestCase):

    def setUp(self):
        # CREATES A TEST DEBATE TO TEST PERCENTAGE SLIDER FUNCTIONALITY
        self.debate = Debate.objects.create(title="Test Debate", content="Content for debate")
    
    def test_get_percentage_existing(self):
        # TESTS THAT WE CAN CALL AN EXISTING PERCENTAGE
        Percentage.objects.create(debate=self.debate, user="testuser", percentage=75)
        url = reverse("get_percentage")
        response = self.client.get(url, {"debateId": self.debate.debateId, "user": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["percentage"], 75)

    def test_add_percentage_new(self):
        # TESTS THAT A USER CAN CREATE A PERCENTAGE SUCCESSFULLY
        url = reverse("add_percentage")  # Updated to match your urlpatterns
        data = {"debateId": self.debate.debateId, "percentage": 85, "user": "testuser"}  # Updated key to match
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Percentage created successfully")

    def test_add_percentage_missing_data(self):
        # EDGE CASE: TESTS THAT IF A REQUEST TO ADD A PERCENTAGE IS SENT WITHOUT DATA, IT FAILS
        url = reverse("add_percentage")
        data = {"debateId": self.debate.debateId}  # Missing percentage and user
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_percentage_not_found(self):
        # EDGE CASE: TEST THAT IF A REQUEST TO GET PERCENTAGE FOR A DEBATE THAT DOESN'T EXIST, IT FAILS
        url = reverse("get_percentage")
        response = self.client.get(url, {"debateId": 999, "user": "nonexistentuser"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBotCommentTests(APITestCase):

    def setUp(self):
        # CREATES A CHATBOT WITH WHICH TO TEST
        self.bot = ChatBot.create_chatbot(bot_id=1, name="TestBot", modelfile="FROM llama3.1")  # Fixed to use create() properly
    
    def test_get_bot_comment(self):
        # TEST THAT THE BOT WILL SUCCESSFULLY RETURN A COMMENT WHEN CALLED
        url = reverse("get_ai_comment")  # Updated to match your urlpatterns
        response = self.client.get(url, {"content": "Give me a bot comment"})  # Adjust as per your expected parameters
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bot_comment", response.data)

        
class GetPinnedDebatesTests(APITestCase):

    def setUp(self):
        # CREATE A TEST USER AND LOG THEM IN
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        self.token = RefreshToken.for_user(self.user).access_token

        # CREATE A TEST DEBATE AND PIN IT FOR THE USER
        self.debate = Debate.objects.create(title="Pinned Debate", content="Content of pinned debate.")
        PinnedDebates.objects.create(user=self.user, debate=self.debate)

    def test_get_pinned_debates(self):
        # TEST THAT PINNED DEBATES CAN BE RETRIEVED CORRECTLY
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse("get_pinned_debates") 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Pinned Debate")
        self.assertEqual(response.data[0]["content"], "Content of pinned debate.")

    def test_get_pinned_debates_unauthenticated(self):
        # EDGE CASE: TEST THAT A USER WHO IS NOT AUTHENTICATED CAN'T RETRIEVE PINNED DEBATES
        self.client.logout()  
        url = reverse("get_pinned_debates")  
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UnpinDebateTests(APITestCase):

    def setUp(self):
        # CREATE A TEST USER AND GENERATE A JWT TOKEN
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token = RefreshToken.for_user(self.user).access_token

        # CREATE A DEBATE AND PIN IT FOR THE USER
        self.debate = Debate.objects.create(title="Pinned Debate", content="Content of pinned debate.")
        self.pinned_debate = PinnedDebates.objects.create(user=self.user, debate=self.debate)

    def test_unpin_debate_success(self):
        # TEST THAT A DEBATE CAN BE SUCCESSFULLY UNPINNED
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        url = reverse("unpin_debate")  
        response = self.client.post(url, {'debateId': self.debate.debateId}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("message"), f"Debate {self.debate.debateId} unpinned successfully")
        self.assertFalse(PinnedDebates.objects.filter(user=self.user, debate=self.debate).exists())

    def test_unpin_nonexistent_pinned_debate(self):
        # EDGE CASE: TEST THAT A WE CANT PIN A NON EXISTANT DEBATE 
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse("unpin_debate")  
        response = self.client.post(url, {'debateId': 9999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json().get("error"), "Pinned debate not found")

    def test_unpin_debate_without_authentication(self):
        # EDGE CASE: SHOULDNT BE ABLE TO UNPIN A DEBATE 
        url = reverse("unpin_debate")
        response = self.client.post(url, {'debateId': self.debate.debateId}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unpin_debate_invalid_request(self):
        # EDGE CASE: INVALID REQUEST FOR PINS
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        url = reverse("unpin_debate") 
        response = self.client.post(url, {}, format='json')  

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("error"), "No debateId provided")