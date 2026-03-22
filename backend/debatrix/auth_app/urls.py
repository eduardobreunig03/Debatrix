from django.urls import path
from .views import StaticSignupView, StaticLoginView, RegisterAPIView, LoginAPIView, UserProfileView, UpdateProfilePictureView, ProfilebyUsernameView

urlpatterns = [
    path('signup/', StaticSignupView.as_view(), name='signup'),
    path('login/', StaticLoginView.as_view(), name='login'),
    path('auth_register/', RegisterAPIView.as_view(), name='register'),
    path('auth_login/', LoginAPIView.as_view(), name='login_api'),
    path('user_profile/', UserProfileView.as_view(), name='profile_api'),
    path('update_profile_picture/', UpdateProfilePictureView.as_view(), name='update_profile_picture'),
    path('userprofilebyUsername/<str:username>/',ProfilebyUsernameView.as_view(),name='userprofilebyUsername')
]
