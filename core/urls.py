from django.urls import path
from .views import (
    ProfileEditAPI,
    SignupAPI,
    UserProfileAPI,
    SpecAPI,
)

urlpatterns = [
    path('user/profile/edit/', ProfileEditAPI.as_view(), name='profile_edit_api'),
    path('user/profile/', UserProfileAPI.as_view(), name='user_profile'),
    path('user/spec/', SpecAPI.as_view(), name='user_spec'),
    path('signup/', SignupAPI.as_view(), name='signup'),
    path('auth/signup/', SignupAPI.as_view(), name='auth_signup'),
]
