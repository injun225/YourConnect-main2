# YourConnectDB

유어커넥트 프로젝트입니도~

*push_all.bat: 폴더에서 이 파일을 더블클릭하면 자동으로 요 깃허브에 커밋, 푸시, 풀 됩니다.
```
작동 순서 : 더블클릭 -> 커밋메세지 작성 -> 엔터(푸시) -> 엔터(작업 종료)
```
*start_all.bat: 폴더에서 이 파일을 더블클릭하면 자동으로 서버가 실행됩니다. 뭔가 꼬이면 밑에 있는 코드 참고!
```
자동으로 창 3개가 뜸:

🧱 Redis 서버

⚙️ Celery 워커

🌐 Django 서버

몇 초 기다리면 http://127.0.0.1:8000 에서 사이트 바로 접속 가능 🎉

```

## 가상환경 + REDIS + CELERY + DJANGO VSCODE에서 실행하는 법

1. 터미널 1에서 redis 실행<Br>
```
redis-server
```
*창에 이렇게 뜨면 정상 ✅<Br>
```
Ready to accept connections tcp<Br>
```
2. 터미널 2에서 가상환경 실행 + Celery 실행<Br>
*프로젝트 폴더 (C:\Users\user\YourConnectDB\career_platform)로 이동한 뒤:
```
.\venv\Scripts\activate
celery -A career_platform worker -l info --pool=solo
```

*아래처럼 “ready” 나오면 성공
```
celery@DESKTOP ready.
   ```
3. 터미널 3에서 DJANGO 서버 실행
```
   (venv) python manage.py runserver
```
이제 http://127.0.0.1:8000 들어가면 Django 웹 서버도 켜짐 ✅

*💡 팁

VSCode 터미널은 여러 개 열 수 있으니까 (+ 버튼 눌러서 새 탭)
각각 Redis / Celery / Django 전용으로 나눠서 두기

이렇게 해두면 PowerShell 따로 안 켜도 구동 가능!!
그냥 VSCode만 켜면 서버 전체 스택이 구동!!




