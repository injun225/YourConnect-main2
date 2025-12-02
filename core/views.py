from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer, UserProfileSerializer, SpecSerializer

User = get_user_model()

# 기존의 UserSignupSerializer 및 SignUpAPI 제거하고 새 SignupAPI 추가
class SignupAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        # 필수 체크
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        account_type = data.get("account_type")   # personal/company

        if not email or not password:
            return Response({"error": "email, password는 필수입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)

        # account_type을 모델의 role로 매핑 (간단 매핑)
        if account_type == "company":
            role_value = "company"
        else:
            role_value = "mentee"

        user = User(
            email=email,
            name=name or "",
            birth=data.get("birth", ""),
            gender=data.get("gender", ""),
            role=role_value,
        )
        user.set_password(password)

        # 추가로 들어오는 필드가 모델에 존재하면 안전하게 세팅
        for key, val in data.items():
            if hasattr(user, key) and key not in {"email", "name", "birth", "gender", "role", "password"}:
                setattr(user, key, val)

        user.save()

        return Response({"message": "회원가입 성공"}, status=status.HTTP_201_CREATED)

# -----------------------------
# 프로필 조회/수정 API
# -----------------------------
class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """프로필 조회"""
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({
            "data": serializer.data,
            "message": "프로필 조회 성공"
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """프로필 수정 (전체)"""
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "프로필이 수정되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "errors": serializer.errors,
            "message": "프로필 수정 실패"
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """프로필 수정 (부분)"""
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "프로필이 수정되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "errors": serializer.errors,
            "message": "프로필 수정 실패"
        }, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# 보유 스펙 조회/수정 API
# -----------------------------
class SpecAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """보유 스펙 조회"""
        user = request.user
        serializer = SpecSerializer(user)
        return Response({
            "data": serializer.data,
            "message": "보유 스펙 조회 성공"
        }, status=status.HTTP_200_OK)

    def put(self, request):
        """보유 스펙 수정 (전체)"""
        user = request.user
        serializer = SpecSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "보유 스펙이 수정되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "errors": serializer.errors,
            "message": "보유 스펙 수정 실패"
        }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """보유 스펙 수정 (부분)"""
        user = request.user
        serializer = SpecSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "보유 스펙이 수정되었습니다."
            }, status=status.HTTP_200_OK)
        return Response({
            "errors": serializer.errors,
            "message": "보유 스펙 수정 실패"
        }, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# 프로필 수정 (로그인 필요)
# -----------------------------
class ProfileEditAPI(APIView):
    permission_classes = [IsAuthenticated]  # JWT 인증 필요

    def post(self, request):
        user = request.user

        spec_job = request.data.get('spec_job')
        desired_job = request.data.get('desired_job')

        if not spec_job and not desired_job:
            return Response(
                {"error": "spec_job 또는 desired_job 중 하나는 포함되어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if spec_job:
            user.spec_job = spec_job

        if desired_job:
            user.desired_job = desired_job

        user.save()

        return Response({
            "message": "Profile updated successfully",
            "user": {
                "email": user.email,
                "spec_job": user.spec_job,
                "desired_job": user.desired_job
            }
        }, status=status.HTTP_200_OK)
