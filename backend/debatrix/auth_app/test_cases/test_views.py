from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from auth_app.models import UserProfile
from rest_framework_simplejwt.tokens import RefreshToken
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from auth_app.validators import CustomPasswordValidator  # Adjust the import as necessary

def generate_image_file():
    # CREATES A NEW TEST IMAGE FILE IN MEMORY FOR USE IN PROFILE PICTURE UPLOAD TEST
    file = BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'jpeg')
    file.seek(0)
    return SimpleUploadedFile('test.jpg', file.read(), content_type='image/jpeg')

class AuthAppViewsTest(APITestCase):
    def setUp(self):
        # INITIALIZES THE TESTING ENVIRONMENT WITH A TEST USER AND ACCESS TOKEN
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='#Password123')
        self.token = RefreshToken.for_user(self.user).access_token

    def test_register_user(self):
        # TESTS THAT A NEW USER CAN REGISTER SUCCESSFULLY AND RECEIVES A VERIFICATION PROMPT
        url = reverse('register')
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "#Password123"
        }
        response = self.client.post(url, data)
        print("RESPONSE") 
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "User registered successfully. Please check your email to verify your account.")

    def test_login_user(self):
        # TESTS THAT AN EXISTING USER CAN LOG IN AND RECEIVE A VALID TOKEN
        url = reverse('login_api')
        data = {
            "username": "testuser",
            "password": "#Password123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_user_profile_view(self):
        # TESTS THAT A USER CAN REQUEST THEIR OWN ACCOUNT DETAILS USING AN AUTH TOKEN
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('profile_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_profile_by_username_view(self):
        # TESTS RETRIEVING A PROFILE BY USERNAME, VERIFIES PROFILE DATA
        url = reverse('userprofilebyUsername', args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)

    def test_update_profile_picture(self):
        # TESTS THAT A USER CAN UPDATE THEIR PROFILE PICTURE SUCCESSFULLY
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        url = reverse('update_profile_picture')
    
        image_file = generate_image_file()
        
        data = {
            "profile_bio": "Updated bio",
            "profile_picture": image_file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile_bio"], "Updated bio")
        self.assertIn("profile_picture", response.data)

class AuthAppPasswordValidatorTests(APITestCase):
    def setUp(self):
        # INITIALIZES THE TEST ENVIRONMENT WITH THE CUSTOM PASSWORD VALIDATOR INSTANCE
        self.validator = CustomPasswordValidator()
    
    def test_password_too_short(self):
        # TESTS THAT PASSWORDS SHORTER THAN THE REQUIRED LENGTH ARE REJECTED
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate("P@ss1")  # Too short
        self.assertEqual(cm.exception.message, "Password must be at least 8 characters long.")
    
    def test_password_no_uppercase(self):
        # TESTS THAT PASSWORDS WITHOUT AN UPPERCASE LETTER ARE REJECTED
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate("password123!")  # No uppercase letter
        self.assertEqual(cm.exception.message, "Password must contain at least one uppercase letter.")
    
    def test_password_no_lowercase(self):
        # TESTS THAT PASSWORDS WITHOUT A LOWERCASE LETTER ARE REJECTED
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate("PASSWORD123!")  # No lowercase letter
        self.assertEqual(cm.exception.message, "Password must contain at least one lowercase letter.")
    
    def test_password_no_digit(self):
        # TESTS THAT PASSWORDS WITHOUT A NUMERIC DIGIT ARE REJECTED
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate("Password!")  # No digit
        self.assertEqual(cm.exception.message, "Password must contain at least one digit.")
    
    def test_password_no_special_character(self):
        # TESTS THAT PASSWORDS WITHOUT A SPECIAL CHARACTER ARE REJECTED
        with self.assertRaises(ValidationError) as cm:
            self.validator.validate("Password123")  # No special character
        self.assertEqual(cm.exception.message, "Password must contain at least one special character.")
    
    def test_valid_password(self):
        # TESTS THAT A VALID PASSWORD PASSES WITHOUT ERROR
        try:
            self.validator.validate("Valid@123")
        except ValidationError:
            self.fail("validate() raised ValidationError unexpectedly!")
