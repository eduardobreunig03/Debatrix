from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from .tokens import email_verification_token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




# Register API
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):   
        print("DATA for SIGNUP ", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #save hashed password
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
  
    
        return Response({
            "message": "User registered successfully. Please check your email to verify your account."
        }, status=status.HTTP_201_CREATED)

     

# Login API
@method_decorator(csrf_exempt, name='dispatch')  # Apply csrf_exempt
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    print("LOGGINGGG IN")
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
    
        if user:
            # token, created = Token.objects.get_or_create(user=user)
            token = get_tokens_for_user(user)
            return Response({
                "message": "User logged in successfully.",
                "user": UserSerializer(user).data,
                "token": token["access"]
            })
        else:
            return Response({
                "message": "Invalid username or password."
            }, status=status.HTTP_401_UNAUTHORIZED)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Assuming the request user is authenticated, you can return their profile
        user = request.user
        # Get the user's profile or create one if it doesn't exist
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        # return the profile picture as a reponse too

        response_data = {
            "username": user.username,
            "email": user.email,
            "profile_picture": user_profile.profile_picture.url if user_profile.profile_picture else None,
            "profile_bio": user_profile.profile_bio,
            # Any other fields you'd like to return
        }
  
        # Return the response directly
        return Response(response_data) 

class ProfilebyUsernameView(APIView):
    def get(self, request, username, *args, **kwargs):
        try:
            print("Username: ", username)
            # Fetch the User instance based on the provided username
            user = User.objects.get(username=username)
            print(f"User found: {user.username}")
            # Retrieve the associated UserProfile instance
            user_profile = UserProfile.objects.get(user=user)
            # Serialize the UserProfile data
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)



# update profile picture
#saving the bio here as well
class UpdateProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("DATA for PROFILE ", request.data)
        user = request.user
        profile_picture = request.FILES.get('profile_picture')  # Fetch the uploaded file
        bio = request.data.get('profile_bio')  # Fetch the bio
        user_profile, created = UserProfile.objects.get_or_create(user=user)  # Get or create the user's profile
        
        # Check if bio is provided and update it
        if bio:
            user_profile.profile_bio = bio
            print(f"Updated bio: {bio}")

        # Check if profile picture is provided and update it
        if profile_picture:
            user_profile.profile_picture = profile_picture
            print(f"Updated profile picture for user: {user.username}")

        # Save the updated profile
        user_profile.save()

        # Prepare the response message based on what was updated
        response_data = {
            "message": "Profile updated successfully.",
            "profile_bio": user_profile.profile_bio,
        }

        # Include profile picture URL if it was updated
        if profile_picture:
            response_data["profile_picture"] = user_profile.profile_picture.url

        return Response(response_data)



# Serving HTML files as static (not recommended for dynamic content)
class StaticSignupView(TemplateView):
    template_name = 'auth_app/signup.html'

class StaticLoginView(TemplateView):
    template_name = 'auth_app/login.html'