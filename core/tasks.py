from celery import shared_task
from .crawler import run_weekly_crawl

@shared_task
def weekly_crawl_task():
    """
    Celery가 주기적으로 실행할 비동기 작업.
    - 매주 월요일 오전 9시마다 자동 실행
    """
    print("[🕘] 주간 크롤링 시작")
    run_weekly_crawl()
    print("[✅] 주간 크롤링 완료")
