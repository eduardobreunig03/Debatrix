from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Debate, Comment, Percentage, PinnedDebates, ChatBot
from django.db import IntegrityError
from django.urls import reverse

class DebateModelTest(TestCase):

    def setUp(self):
        # SETS UP ENVIRONMENT BY CREATING A TEST USER AND TEST DEBATE AUTHORED BY THE USER
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.debate = Debate.objects.create(
            creatorUserName=self.user.username,
            title="DEBATE 1",
            content="DEBATE CONTENT",
        )

    def test_debate_id_autoincrement(self):
        # ENSURE DEBATEID IS AUTO-ASSIGNED AND INCREMENTS CORRECTLY.
        debate2 = Debate.objects.create(
            creatorUserName=self.user.username,
            title="DEBATE 2",
            content="DEBATE CONTENT 2",
        )
        self.assertEqual(debate2.debateId, self.debate.debateId + 1)

    def test_comment_count(self):
        # TEST COUNTING COMMENTS FOR A DEBATE.
        Comment.objects.create(parent_debate=self.debate, user=self.user, content="COMMENT 1")
        Comment.objects.create(parent_debate=self.debate, user=self.user, content="COMMENT 2")
        self.debate.get_comment_count()
        self.assertEqual(self.debate.numberComments, 2)
    
    def test_queryset_filtering(self):
        # TEST FILTERING DEBATES BASED ON SEARCH QUERY.
        url = reverse('debates')
        response = self.client.get(url, {'search': 'DEBATE 1'})  # SIMULATE A GET REQUEST WITH SEARCH PARAM
        self.assertEqual(response.status_code, 200)  # CHECK IF THE RESPONSE IS OK
        self.assertEqual(len(response.data), 1)  # EXPECTING 1 DEBATE TO MATCH
        self.assertEqual(response.data[0]['title'], 'DEBATE 1')

        # TEST WITH A SEARCH QUERY THAT MATCHES NO DEBATES
        response = self.client.get(url, {'search': 'NON-EXISTENT DEBATE'})
        self.assertEqual(len(response.data), 0)  # EXPECTING NO DEBATES TO MATCH


class CommentModelTest(TestCase):
    def setUp(self):
        # SETS UP ENVIRONMENT BY CREATING A TEST USER AND TEST DEBATE AUTHORED BY THE USER
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.debate = Debate.objects.create(
            creatorUserName=self.user.username,
            title="DEBATE 1",
            content="DEBATE CONTENT",
        )
    
    def test_create_comment(self):
        # TEST COMMENT CREATION AND STRING REPRESENTATION.
        comment = Comment.objects.create(parent_debate=self.debate, user=self.user, content="A SAMPLE COMMENT")
        self.assertEqual(str(comment), f"{self.user.username}: A SAMPLE COMMENT")
        self.assertEqual(comment.depth, 0)

    def test_comment_reply(self):
        # TEST PARENT-CHILD RELATIONSHIP IN COMMENTS.
        parent_comment = Comment.objects.create(parent_debate=self.debate, user=self.user, content="PARENT COMMENT")
        reply_comment = Comment.objects.create(parent_debate=self.debate, parent_comment=parent_comment, user=self.user, content="REPLY COMMENT")
        self.assertEqual(reply_comment.parent_comment, parent_comment)

class PercentageModelTest(TestCase):
    def setUp(self):
        # SETS UP ENVIRONMENT BY CREATING A TEST USER AND TEST DEBATE AUTHORED BY THE USER
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.debate = Debate.objects.create(
            creatorUserName=self.user.username,
            title="DEBATE 1",
            content="DEBATE CONTENT",
        )

    def test_unique_user_debate_percentage(self):
        # ENSURE A USER CANNOT RATE THE SAME DEBATE MORE THAN ONCE.
        Percentage.objects.create(user=self.user.username, debate=self.debate, percentage=70)
        with self.assertRaises(IntegrityError):
            Percentage.objects.create(user=self.user.username, debate=self.debate, percentage=85)

class PinnedDebatesModelTest(TestCase):
    def setUp(self):
        # SETS UP ENVIRONMENT BY CREATING A TEST USER AND TEST DEBATE AUTHORED BY THE USER
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.debate = Debate.objects.create(
            creatorUserName=self.user.username,
            title="DEBATE 1",
            content="DEBATE CONTENT",
        )
    
    def test_pinning_debate(self):
        # TEST PINNING A DEBATE AND ITS STRING REPRESENTATION.
        pinned_debate = PinnedDebates.objects.create(debate=self.debate, user=self.user)
        self.assertEqual(str(pinned_debate), f"{self.user.username} PINNED {self.debate.title}")

class ChatBotModelTest(TestCase):
    def test_create_chatbot_params(self):
        # TEST CHATBOT CREATION AND ATTRIBUTES.
        bot = ChatBot.create_chatbot(bot_id=1, name="TESTBOT", modelfile="FROM LLAMA3.1")
        self.assertEqual(bot.name, "TESTBOT")
        self.assertEqual(bot.modelfile, "FROM LLAMA3.1")
        self.assertEqual(bot.bot_id, 1)

    def test_create_chatbot_exists(self):
        # TESTS IF CHATBOT EXISTS IN DATABASE AFTER CREATION
        bot = ChatBot.create_chatbot(bot_id=5, name="TESTBOT", modelfile="FROM LLAMA3.1")           
        self.assertTrue(ChatBot.objects.filter(bot_id=bot.bot_id).exists())

    def test_creating_chatbot_user(self):
        # TESTS THAT THE USER FOR A GIVEN CHATBOT IS CREATED SUCCESSFULLY
        bot = ChatBot.objects.create(bot_id=9, name="TESTBOT", modelfile="FROM LLAMA3.1")
        ChatBot.create_user_for_chatbot(bot)
        self.assertIsNotNone(bot.user)
        self.assertTrue(bot.user in User.objects.all())
