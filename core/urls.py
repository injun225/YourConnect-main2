from django.urls import path
from .views import (
    ProfileEditAPI,
    SignupAPI,
)

urlpatterns = [
    path('user/profile/edit/', ProfileEditAPI.as_view(), name='profile_edit_api'),
    path('signup/', SignupAPI.as_view(), name='signup'),
    path('auth/signup/', SignupAPI.as_view(), name='auth_signup'),  # 추가: 필요 시 별칭으로 사용
]
