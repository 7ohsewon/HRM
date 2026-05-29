# 📚 교육 대시보드 (Streamlit 버전)

직원 교육 이수 현황을 간단하게 관리할 수 있는 Streamlit 기반 웹 애플리케이션입니다.

## 🌟 특징

### 🎨 HD현대 디자인 시스템
- **프리미엄 색상 팔레트**: 진한 네이비(#003DA5) 기반 전문적 이미지
- **현대적 UI/UX**: 그래디언트 배경, 부드러운 애니메이션, 호버 효과
- **반응형 디자인**: 모든 디바이스에서 최적화된 화면 제공
- **일관된 스타일**: 카드, 버튼, 배지, 진행률 바까지 통일된 디자인

### ✨ 간단한 배포
- Streamlit Community Cloud에 한 번의 클릭으로 배포
- 자동 CI/CD (GitHub 연동)
- 별도의 호스팅 비용 없음 (무료)

### 👥 역할 기반 접근
- **관리자**: 교육 관리, 이수 현황 입력, 자율교육 승인
- **직원**: 교육 현황 조회, 자율교육 신청

### 📊 주요 기능
- 기본교육 관리
- 자율교육 신청 및 승인
- 교육 현황 대시보드 (진행률 시각화)
- 통계 및 분석
- **CSV 일괄 임포트** (기존 훈련 데이터)

## 🛠️ 기술 스택

| 계층 | 기술 |
|------|------|
| **Framework** | Streamlit |
| **Language** | Python 3.10+ |
| **Database** | SQLite (로컬) / PostgreSQL (선택) |
| **Deployment** | Streamlit Community Cloud |
| **Auth** | bcrypt + JWT |

## 🚀 빠른 시작

### 로컬 실행

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/education-dashboard-streamlit.git
cd education-dashboard-streamlit

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run app.py

# 4. 브라우저에서 접속
# http://localhost:8501
```

### Streamlit.io에 배포

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://education-dashboard-streamlit.streamlit.app)

**배포 가이드**: [STREAMLIT_DEPLOY.md](STREAMLIT_DEPLOY.md)

## 👤 테스트 계정

| 역할 | 직번 | 비밀번호 |
|------|------|---------|
| 관리자 | 001 | 001 |
| 직원1 | 002 | 002 |
| 직원2 | 003 | 003 |
| 직원3 | 004 | 004 |

## 📁 파일 구조

```
education-dashboard-streamlit/
├── app.py                          # 메인 애플리케이션
├── requirements.txt                # Python 의존성
├── .streamlit/
│   └── config.toml                # Streamlit 설정
├── .gitignore
├── README.md                       # 이 파일
└── STREAMLIT_DEPLOY.md             # 배포 가이드
```

## 📦 주요 라이브러리

```
streamlit==1.31.1          # 웹 프레임워크
pandas==2.1.3              # 데이터 분석
plotly==5.18.0             # 인터랙티브 차트
sqlalchemy==2.0.23         # ORM
bcrypt==4.1.1              # 비밀번호 암호화
pyjwt==2.8.1               # 토큰 관리
```

## 🔐 초기 설정

### 1. 샘플 데이터 생성

앱 첫 실행 시 자동으로 다음이 생성됩니다:
- 4명의 샘플 사용자
- 4개의 기본교육
- 교육 이수 기록

### 2. 비밀번호 변경 (선택)

로그인 후 설정에서 비밀번호 변경 가능:
- 초기값: `직번`
- 예: 직번 001 → 초기 비밀번호 001

### 3. 데이터베이스

- **로컬**: SQLite (`education_dashboard.db`)
- **배포**: Streamlit Secrets에 PostgreSQL URL 저장 가능

## 🎯 주요 기능

### 관리자 기능
- ✅ 기본교육 생성/수정/삭제
- ✅ 직원 이수 현황 입력
- ✅ 자율교육 승인/거절
- ✅ 전사 통계 및 리포트

### 직원 기능
- ✅ 교육 현황 조회
- ✅ 자율교육 신청
- ✅ 증빙 파일 업로드
- ✅ 개인 대시보드

## 📊 데이터 구조

### users 테이블
```
user_id (PK) | name    | password | role     | department
001           | 관리자  | hash... | admin    | 인사팀
002           | 김직원  | hash... | employee | 영업팀
```

### mandatory_training 테이블
```
id | training_name | description  | year
1  | 신입직원 교육  | ...         | 2024
2  | 안전보건 교육  | ...         | 2024
```

### autonomous_training 테이블
```
id | user_id | training_name | provider | status   | submitted_date
1  | 002     | React 기초    | Udemy    | pending  | 2024-05-29
```

## 🎨 디자인 시스템

### HD현대 색상 팔레트
```
Primary Colors:
  - Navy Blue: #003DA5 (주요 색상)
  - Dark Navy: #002D7F (호버 상태)
  - Primary Light: #1A4B8C

Accent Colors:
  - Bright Blue: #3B82F6 (강조)
  - Green: #22C55E (완료/성공)
  - Teal: #0E7490 (정보)

Neutral:
  - Dark Surface: #0F172A (어두운 배경)
  - White Canvas: #FFFFFF (밝은 배경)
  - Muted: #64748B (보조 텍스트)
```

### UI Components
- **헤로 밴드**: 큰 제목과 부제목용 그래디언트 배경
- **메트릭 카드**: 통계 표시용 카드 (호버 효과 포함)
- **프로그레스 바**: 교육 이수율 시각화
- **상태 배지**: 이수/대기/거절 상태 표시
- **버튼**: HD Navy 기본 + 호버 시 진한 색상

## 🔧 개발 팁

### 로컬 테스트
```bash
# 개발 모드 (자동 재로드)
streamlit run app.py --logger.level=debug
```

### DB 초기화
```bash
# 기존 DB 삭제
rm education_dashboard.db

# 재실행하면 새 DB 생성
streamlit run app.py
```

### 패키지 업데이트
```bash
pip install --upgrade streamlit pandas plotly
pip freeze > requirements.txt
```

## 📱 모바일 호환성

Streamlit은 자동으로 반응형 디자인을 제공합니다:
- 모바일, 태블릿, 데스크톱 모두 지원
- 모바일에서도 모든 기능 사용 가능

## 🚨 주의사항

1. **데이터 영구성**: 
   - SQLite는 로컬에서만 작동
   - Streamlit 배포 시 재부팅마다 데이터 초기화됨
   - **해결책**: PostgreSQL 같은 외부 DB 사용

2. **파일 업로드**:
   - 현재 메모리 기반 처리
   - 영구 저장을 위해 AWS S3 등 연동 필요

3. **세션 관리**:
   - Streamlit 기본 세션 사용
   - 고급 세션 관리가 필요하면 커스터마이징 필요

## 🔐 보안

- ✅ bcrypt로 비밀번호 해싱
- ✅ JWT 토큰 (선택)
- ✅ 역할 기반 접근 제어
- ✅ 환경 변수로 민감한 정보 관리

**할 일**:
- [ ] HTTPS 전용 (streamlit.io에서 자동 제공)
- [ ] CSRF 방지
- [ ] Rate limiting
- [ ] 감사 로그

## 📈 성능

- 초기 로드: ~2초
- 페이지 전환: ~1초
- 데이터 조회: ~500ms
- 배포 초기화: ~1분

## 🎓 학습 자료

- [Streamlit 공식 튜토리얼](https://docs.streamlit.io/library/get-started)
- [Streamlit API 레퍼런스](https://docs.streamlit.io/library/api-reference)
- [커뮤니티 Q&A](https://discuss.streamlit.io)

## 🐛 이슈 및 개선사항

### 예정된 기능
- [ ] PostgreSQL 풀 지원
- [ ] 이메일 알림
- [ ] 엑셀 내보내기
- [ ] 고급 검색 필터
- [ ] 교육 일정 관리

### 알려진 이슈
- SQLite 데이터 영구성 (배포 시)
- 대용량 파일 업로드 제한

## 📞 지원

- 🐛 버그 리포트: GitHub Issues
- 💬 기능 제안: GitHub Discussions
- 📧 문의: admin@example.com

## 📄 라이선스

내부 사용 전용

---

## 🎉 배포 완료!

```bash
# GitHub에 푸시
git add .
git commit -m "Initial Streamlit deployment"
git push origin main

# 자동으로 배포됨:
# https://education-dashboard-streamlit.streamlit.app
```

**축하합니다!** 이제 누구나 온라인에서 접속 가능한 교육 대시보드를 갖게 되었습니다! 🚀

---

**마지막 업데이트**: 2026-05-29  
**버전**: 1.2.0 (HD현대 디자인 시스템 적용)

### 최근 업데이트
- ✅ HD현대 디자인 시스템 전체 적용
- ✅ CSV 일괄 임포트 기능 추가
- ✅ 진행률 시각화 (프로그레스 바)
- ✅ 향상된 메트릭 카드 UI
- ✅ 부드러운 애니메이션 및 호버 효과
