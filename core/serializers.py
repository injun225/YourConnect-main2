from rest_framework import serializers
from .models import User

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
            "birth",
            "gender",
            "role",
            "agree_age",
            "agree_service",
            "agree_personal_info",
            "agree_ad"
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "birth",
            "gender",
            "role", 
            "agree_age",
            "agree_service",
            "agree_personal_info",
            "agree_ad",
            "is_active"
        ]
        read_only_fields = ["id", "email", "is_active"]

    def validate_birth(self, value):
        # birth 형식 검증 (YYYY-MM-DD)
        if value and len(value) != 10:
            raise serializers.ValidationError("생년월일은 YYYY-MM-DD 형식이어야 합니다.")
        return value

    def validate_gender(self, value):
        # gender 유효한 선택지 확인
        valid_choices = ["female", "male"]
        if value and value not in valid_choices:
            raise serializers.ValidationError("성별은 'female' 또는 'male'이어야 합니다.")
        return value

class SpecSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "job",
            "job_detail",
            "job_level",
            "company_type",
            "experience_years",
            "region",
            "company_name"
        ]
        read_only_fields = ["id"]

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError("경력은 0 이상이어야 합니다.")
        return value
