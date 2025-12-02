# 인준 커밋
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 사용자 매니저
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


# ✅ 1️⃣ 사용자(User)
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("mentee", "일반"),
        ("mentor", "멘토"),
        ("company", "기업"),
    )

    GENDER_CHOICES = (
        ("female", "여자"),
        ("male", "남자"),
    )

    JOB_CHOICES = (
        ("개발", "개발"),
        ("데이터", "데이터"),
        ("인공지능/머신러닝", "인공지능/머신러닝"),
        ("디자인", "디자인"),
        ("QA/테스트", "QA/테스트"),
    )

    JOB_LEVEL_CHOICES = (
        ("신입", "신입"),
        ("주임", "주임"),
        ("대리", "대리"),
        ("과장", "과장"),
        ("차장", "차장"),
        ("부장", "부장"),
        ("임원", "임원"),
    )

    COMPANY_TYPE_CHOICES = (
        ("대기업", "대기업"),
        ("중견기업", "중견기업"),
        ("중소기업", "중소기업"),
        ("외국계", "외국계"),
        ("공기업", "공기업"),
        ("벤처기업", "벤처기업"),
    )

    REGION_CHOICES = (
        ("서울", "서울"),
        ("경기", "경기"),
        ("인천", "인천"),
        ("대전", "대전"),
        ("세종", "세종"),
        ("충남", "충남"),
        ("충북", "충북"),
        ("광주", "광주"),
        ("전남", "전남"),
        ("전북", "전북"),
        ("대구", "대구"),
        ("경북", "경북"),
        ("경남", "경남"),
        ("부산", "부산"),
        ("울산", "울산"),
        ("강원", "강원"),
        ("제주", "제주"),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    birth = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # 보유 스펙 정보
    job = models.CharField(max_length=50, choices=JOB_CHOICES, null=True, blank=True, verbose_name="직무")
    job_detail = models.CharField(max_length=100, null=True, blank=True, verbose_name="세부 직무")
    job_level = models.CharField(max_length=20, choices=JOB_LEVEL_CHOICES, null=True, blank=True, verbose_name="직급")
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, null=True, blank=True, verbose_name="기업형태")
    experience_years = models.IntegerField(default=0, verbose_name="경력")
    region = models.CharField(max_length=50, null=True, blank=True, verbose_name="근무지역")
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="회사명")

    # 약관 동의
    agree_age = models.BooleanField(default=False)
    agree_service = models.BooleanField(default=False)
    agree_personal_info = models.BooleanField(default=False)
    agree_ad = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# ✅ 2️⃣ 멤버십 요금제
class Membership(models.Model):
    STATUS_CHOICES = [
        ('활성', '활성'),
        ('비활성', '비활성'),
    ]
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.TextField(blank=True, null=True)
    duration_month = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='활성')

    def __str__(self):
        return self.name


# ✅ 3️⃣ 경력 정보
class Experience(models.Model):
    CAREER_TYPE_CHOICES = [
        ('정규직', '정규직'),
        ('인턴', '인턴'),
        ('프로젝트', '프로젝트'),
        ('기타', '기타'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    career_type = models.CharField(max_length=20, choices=CAREER_TYPE_CHOICES, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} - {self.role}"


# ✅ 4️⃣ 채팅방
class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Chat #{self.id}"


# ✅ 5️⃣ 채팅 참여자
class ChatParticipant(models.Model):
    ROLE_CHOICES = [
        ('멘토', '멘토'),
        ('멘티', '멘티'),
    ]
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('chat', 'user')

    def __str__(self):
        return f"{self.user.name or self.user.email} in Chat {self.chat.id}"


# ✅ 6️⃣ 채팅 메시지
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.sender.name or self.sender.email} ({self.chat.id})"


# ✅ 7️⃣ AI 피드백 로그
class AiFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"AI Feedback - {self.user.name or self.user.email}"


# ✅ 8️⃣ 멘토링 예약
class MentorSession(models.Model):
    STATUS_CHOICES = [
        ('예약', '예약'),
        ('완료', '완료'),
        ('취소', '취소'),
    ]
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_sessions')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_sessions')
    schedule_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='예약')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Session {self.id} ({self.mentor.name or self.mentor.email} ↔ {self.mentee.name or self.mentee.email})"


# ✅ 9️⃣ 채용공고
class JobPost(models.Model):
    STATUS_CHOICES = [
        ('모집중', '모집중'),
        ('마감', '마감'),
        ('비공개', '비공개'),
    ]
    JOB_TYPE_CHOICES = [
        ('정규직', '정규직'),
        ('인턴', '인턴'),
        ('계약직', '계약직'),
        ('프리랜서', '프리랜서'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='정규직')
    location = models.CharField(max_length=100, blank=True, null=True)
    salary = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    skills = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='모집중')
    def __str__(self):
        return f"{self.title} ({self.company})"


# ✅ 🔟 채용 지원 내역
class JobApplication(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_link = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.name or self.user.email} → {self.job.title}"


# ✅ 11. 공고 북마크
class JobBookmark(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'user')

    def __str__(self):
        return f"{self.user.name or self.user.email} bookmarked {self.job.title}"