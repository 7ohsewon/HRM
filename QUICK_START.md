# ⚡ Streamlit 배포 30초 가이드

## 📋 배포 체크리스트

### ✅ 1단계: 사전 준비 (5분)

```bash
# 필수 설치
# - Git (https://git-scm.com)
# - GitHub 계정 (https://github.com)
# - Streamlit 계정 (https://share.streamlit.io)
```

### ✅ 2단계: 파일 준비

현재 폴더에 다음 파일이 있는지 확인:
```
✓ app.py
✓ requirements.txt
✓ .streamlit/config.toml
✓ .gitignore
✓ README.md
```

### ✅ 3단계: GitHub 저장소 생성 (3분)

```bash
# 터미널에서 실행
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/education-dashboard-streamlit.git
git push -u origin main
```

**결과**: GitHub 저장소가 생성됨

### ✅ 4단계: Streamlit에 배포 (2분)

1. https://share.streamlit.io 방문
2. GitHub으로 로그인
3. "New app" 클릭
4. 다음 입력:
   - **Repository**: `YOUR_USERNAME/education-dashboard-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. "Deploy!" 클릭

**결과**: 앱이 배포됨 (1-2분 소요)

---

## 🔗 배포 완료!

```
https://education-dashboard-streamlit.streamlit.app
```

또는 당신의 커스텀 도메인:
```
https://your-custom-domain.streamlit.app
```

---

## 👤 로그인 테스트

| 계정 | 직번 | 비밀번호 |
|------|------|---------|
| 관리자 | 001 | 001 |
| 직원 | 002 | 002 |

---

## 🔄 코드 업데이트 후 재배포

```bash
git add .
git commit -m "Update features"
git push

# 자동으로 배포됨 (1-2분 후)
```

---

## 🐛 배포 문제 해결

### 앱이 안 열려요
1. https://share.streamlit.io/YOUR_USERNAME/education-dashboard-streamlit 확인
2. GitHub 저장소 접근 권한 확인
3. `app.py` 위치 확인

### 라이브러리 오류
```bash
# requirements.txt 재생성
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### 데이터가 초기화돼요
현재는 SQLite 메모리 기반입니다. PostgreSQL 연동이 필요하면:
1. `.streamlit/secrets.toml` 생성
2. PostgreSQL URL 추가
3. `app.py`에서 PostgreSQL 연동

---

## 📚 상세 가이드

- [전체 배포 가이드](STREAMLIT_DEPLOY.md)
- [프로젝트 README](README.md)
- [Streamlit 공식 문서](https://docs.streamlit.io)

---

## 💡 팁

✨ **GitHub 저장소 URL 형식**:
```
https://github.com/YOUR_USERNAME/education-dashboard-streamlit
```

✨ **배포 URL 자동 생성**:
```
https://share.streamlit.io/YOUR_USERNAME/education-dashboard-streamlit/main/app.py
```

✨ **Streamlit Community Cloud 대시보드**:
```
https://share.streamlit.io
```

---

## ⏱️ 예상 시간

- 저장소 생성: 3분
- Streamlit 배포: 2분
- 앱 빌드 및 배포: 1-2분
- **총 시간: 약 10분** ⚡

---

**이제 준비 완료! GitHub에 푸시하면 자동으로 배포됩니다!** 🚀

```bash
git push origin main
```

---

📧 문제가 발생하면:
1. GitHub Issues에 버그 리포트
2. Streamlit 커뮤니티 포럼에서 질문
3. 관리자에게 문의

**축하합니다! 앱이 배포되었습니다!** 🎉
