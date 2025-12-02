import requests
from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
import json
import os

User = get_user_model()


def build_query_for_user(user):
    """사용자 스펙 + 희망직무로 검색어 생성"""
    if not user.spec_job and not user.desired_job:
        return None
    return f"{user.spec_job or ''} {user.desired_job or ''} 채용공고".strip()


def crawl_jobs(keyword):
    """사람인 채용공고 크롤링 (307 우회 버전)"""
    url = f"https://www.saramin.co.kr/zf_user/search?searchword={keyword}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.saramin.co.kr/",
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;"
            "q=0.8,application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
    }

    session = requests.Session()
    response = session.get(url, headers=headers, allow_redirects=True)

    if response.status_code != 200:
        print(f"[⚠️] 요청 실패 ({response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for item in soup.select("h2 > a"):
        title = item.text.strip()
        link = "https://www.saramin.co.kr" + item.get("href", "")
        jobs.append({"title": title, "link": link})

    return jobs


def run_weekly_crawl():
    """전체 사용자 정보를 읽어서 크롤링 실행"""
    users = User.objects.all()
    base_dir = os.path.join(os.getcwd(), "crawl_results")
    os.makedirs(base_dir, exist_ok=True)

    for user in users:
        query = build_query_for_user(user)
        if not query:
            print(f"[⚠️] {user.username}: 선택값 없음, 건너뜀")
            continue

        results = crawl_jobs(query)
        save_path = os.path.join(base_dir, f"results_{user.username}.json")

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"[💾] {user.username}: {len(results)}건 저장 완료")
