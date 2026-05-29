# 📱 Streamlit 배포 가이드

Streamlit으로 만든 교육 대시보드를 **Streamlit Community Cloud**에 무료로 배포합니다.

## 🚀 배포 단계

### 1단계: GitHub 저장소 생성

```bash
# 프로젝트 초기화
cd education-dashboard-streamlit
git init
git add .
git commit -m "Initial commit"

# GitHub에 푸시
git remote add origin https://github.com/your-username/education-dashboard-streamlit.git
git branch -M main
git push -u origin main
```

### 2단계: Streamlit Community Cloud 가입

1. https://share.streamlit.io 방문
2. "Sign up" 클릭
3. GitHub 계정으로 로그인

### 3단계: 앱 배포

1. Streamlit Community Cloud 대시보드에서 **"New app"** 클릭
2. 다음 정보 입력:
   - **Repository**: `your-username/education-dashboard-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`

3. **Deploy!** 클릭

### 4단계: 배포 완료

몇 초 후 앱이 자동으로 배포됩니다:
```
https://education-dashboard-streamlit.streamlit.app
```

---

## 📋 파일 구조

```
education-dashboard-streamlit/
├── app.py                      # 메인 애플리케이션
├── requirements.txt            # Python 의존성
├── .streamlit/
│   └── config.toml            # Streamlit 설정
├── .gitignore
├── README.md
└── STREAMLIT_DEPLOY.md        # 이 파일
```

---

## 🔧 로컬 실행

개발 중에 로컬에서 테스트하려면:

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. Streamlit 실행
streamlit run app.py

# 3. 브라우저에서 접속
# http://localhost:8501
```

---

## 📝 초기 테스트 계정

| 역할 | 직번 | 비밀번호 |
|------|------|---------|
| 관리자 | 001 | 001 |
| 직원 | 002 | 002 |
| 직원 | 003 | 003 |
| 직원 | 004 | 004 |

---

## 🔄 자동 배포 설정

GitHub에 푸시하면 자동으로 배포됩니다:

```bash
# 코드 수정 후
git add .
git commit -m "Update features"
git push

# 자동으로 streamlit.io에 배포됨 (1-2분 후)
```

---

## ⚙️ 환경 변수 설정 (선택)

민감한 정보는 Streamlit Community Cloud에서 환경 변수로 설정:

1. 앱 설정 → Secrets 메뉴
2. `.streamlit/secrets.toml` 형식으로 입력:
   ```toml
   db_host = "your-db-host"
   db_password = "your-password"
   jwt_secret = "your-secret"
   ```

3. 코드에서 접근:
   ```python
   import streamlit as st
   db_password = st.secrets["db_password"]
   ```

---

## 📱 모바일 접속

배포된 앱은 모바일에서도 접속 가능합니다:
- 링크 공유: https://education-dashboard-streamlit.streamlit.app
- 반응형으로 자동 조정됨

---

## 🐛 문제 해결

### 앱이 로드되지 않음
- GitHub 저장소 접근 권한 확인
- `app.py` 파일 위치 확인
- Logs 탭에서 에러 메시지 확인

### 라이브러리 설치 오류
- `requirements.txt`에 모든 의존성 포함 확인
- 버전 호환성 확인:
  ```bash
  pip freeze > requirements.txt
  ```

### 데이터베이스 오류
- SQLite는 메모리 기반이므로 재배포 시 데이터 초기화됨
- 영구 저장을 원하면 PostgreSQL 등 외부 DB 사용 필요

---

## 💾 데이터 저장 (선택)

### 옵션 1: PostgreSQL 사용

```python
import psycopg2
from sqlalchemy import create_engine

# secrets.toml
database_url = st.secrets["database_url"]

# 코드
engine = create_engine(database_url)
```

### 옵션 2: Google Sheets 사용

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

credentials = st.secrets["google_credentials"]
```

---

## 📊 배포 후 모니터링

Streamlit Community Cloud 대시보드에서:
- 📈 트래픽 통계
- 🔧 로그 확인
- 🔄 배포 이력
- ⚠️ 에러 알림

---

## 🔒 보안 팁

1. ✅ 민감한 정보는 `.env` / `secrets.toml`에 저장
2. ✅ GitHub에 `credentials.json` 업로드 금지
3. ✅ `.gitignore` 설정:
   ```
   .streamlit/secrets.toml
   *.db
   __pycache__/
   .env
   ```
4. ✅ 정기적으로 의존성 업데이트

---

## 📚 추가 리소스

- [Streamlit 공식 문서](https://docs.streamlit.io)
- [Streamlit Community Cloud](https://share.streamlit.io)
- [Streamlit GitHub](https://github.com/streamlit/streamlit)

---

## 🎯 다음 단계

1. 현재 Streamlit 앱 배포 (기본 기능)
2. 모든 페이지 구현 (대시보드, 관리, 통계)
3. PostgreSQL 연동 (데이터 영구 저장)
4. 커스텀 도메인 설정 (선택)

---

**배포 완료 후 링크 공유**: https://education-dashboard-streamlit.streamlit.app

🎉 축하합니다! 이제 누구나 온라인에서 교육 대시보드를 사용할 수 있습니다!
