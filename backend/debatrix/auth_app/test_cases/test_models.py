from django.test import TestCase
from django.contrib.auth.models import User
from auth_app.models import UserProfile

class UserProfileModelTest(TestCase):
    # SETTING UP ENVIRONMENT
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)

    # SIMPLE USER CREATION TEST 
    def test_user_profile_creation(self):
        # test that a new user is able to be created
        self.assertEqual(self.user_profile.user, self.user)
        self.assertFalse(self.user_profile.profile_picture)  
        self.assertIsNone(self.user_profile.profile_bio)

    # TESTS IF STRING REPRESENTATION IS WORKING PROPERLY
    def test_user_profile_str_representation(self):
        self.assertEqual(str(self.user_profile), "testuser's Profile")

    # TESTING PROFILE BIO
    def test_update_profile_bio(self):
        bio_text = "This is a test bio."
        self.user_profile.profile_bio = bio_text
        self.user_profile.save()
        self.assertEqual(self.user_profile.profile_bio, bio_text)

    # EDGE CASE: PROFILE BIO EMPTY 
    def test_update_profile_bio_empty(self):
        bio_text = ""
        self.user_profile.profile_bio = bio_text
        self.user_profile.save()
        self.assertEqual(self.user_profile.profile_bio, bio_text)
