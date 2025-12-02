import os
from celery import Celery
from celery.schedules import crontab

# Django 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "career_platform.settings")

app = Celery("career_platform")

# Django 설정에서 CELERY 관련 항목 자동 로드
app.config_from_object("django.conf:settings", namespace="CELERY")

# 모든 앱의 tasks.py 자동 검색
app.autodiscover_tasks()

# 🔁 매주 월요일 오전 9시에 실행되도록 스케줄링
app.conf.beat_schedule = {
     "weekly-crawl-every-monday-9am": {
        "task": "core.tasks.weekly_crawl_task",  # 🔥 여기만 core로!
        "schedule": crontab(hour=9, minute=0, day_of_week=1),  # 월요일 09:00
    },
}
