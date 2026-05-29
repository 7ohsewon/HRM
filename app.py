import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import hashlib
import os

# 페이지 설정
st.set_page_config(
    page_title="교육 대시보드",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일
st.markdown("""
    <style>
    .main {
        padding-top: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.role = None

# DB 함수
def init_db():
    conn = sqlite3.connect('education_dashboard.db')
    c = conn.cursor()

    # 사용자 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id TEXT PRIMARY KEY,
                  name TEXT,
                  password TEXT,
                  role TEXT,
                  department TEXT)''')

    # 기본교육 테이블
    c.execute('''CREATE TABLE IF NOT EXISTS mandatory_training
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  training_name TEXT,
                  description TEXT,
                  year INTEGER)''')

    # 기본교육 이수 현황
    c.execute('''CREATE TABLE IF NOT EXISTS mandatory_records
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT,
                  training_id INTEGER,
                  status TEXT,
                  score INTEGER,
                  completion_date TEXT,
                  UNIQUE(user_id, training_id))''')

    # 자율교육
    c.execute('''CREATE TABLE IF NOT EXISTS autonomous_training
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT,
                  training_name TEXT,
                  provider TEXT,
                  training_date TEXT,
                  description TEXT,
                  status TEXT,
                  submitted_date TEXT)''')

    conn.commit()
    return conn

# 초기 데이터 생성
def create_sample_data():
    conn = init_db()
    c = conn.cursor()

    try:
        # 샘플 사용자
        users = [
            ('001', '관리자', hashlib.sha256('001'.encode()).hexdigest(), 'admin', '인사팀'),
            ('002', '김직원', hashlib.sha256('002'.encode()).hexdigest(), 'employee', '영업팀'),
            ('003', '이직원', hashlib.sha256('003'.encode()).hexdigest(), 'employee', '개발팀'),
            ('004', '박직원', hashlib.sha256('004'.encode()).hexdigest(), 'employee', '마케팅팀'),
        ]

        for user in users:
            c.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)', user)

        # 샘플 교육
        trainings = [
            ('신입직원 교육', '신입직원 대상 기본 교육', 2024),
            ('안전보건 교육', '직장 안전보건 교육', 2024),
            ('성희롱 예방 교육', '성희롱 및 성폭력 예방 교육', 2024),
            ('개인정보보호 교육', '개인정보보호법 교육', 2024),
        ]

        for training in trainings:
            c.execute('INSERT OR IGNORE INTO mandatory_training (training_name, description, year) VALUES (?, ?, ?)', training)

        conn.commit()
    except:
        pass
    finally:
        conn.close()

# 로그인 함수
def login(user_id, password):
    conn = init_db()
    c = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    c.execute('SELECT * FROM users WHERE user_id = ? AND password = ?', (user_id, password_hash))
    user = c.fetchone()
    conn.close()

    return user

# 페이지 라우팅
if not st.session_state.logged_in:
    # 로그인 페이지
    st.title("📚 교육 대시보드")
    st.subtitle("직원 교육참여 실적 관리 시스템")

    create_sample_data()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("👤 계정 정보\n\n**관리자**: 001 / 001\n\n**직원**: 002~004 / 002~004")

    with col2:
        st.warning("⚠️ 초기 비밀번호\n\n직번과 동일한 숫자를 입력하세요")

    st.divider()

    with st.form("login_form"):
        col1, col2 = st.columns(2)

        with col1:
            user_id = st.text_input("직번", placeholder="직번 입력")

        with col2:
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력")

        submitted = st.form_submit_button("🔐 로그인", use_container_width=True)

        if submitted:
            if not user_id or not password:
                st.error("직번과 비밀번호를 입력해주세요.")
            else:
                user = login(user_id, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.role = user[3]  # role
                    st.rerun()
                else:
                    st.error("직번 또는 비밀번호가 맞지 않습니다.")

else:
    # 헤더
    col1, col2 = st.columns([5, 1])

    with col1:
        st.title("📊 교육 대시보드")

    with col2:
        if st.button("🚪 로그아웃", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    # 사용자 정보
    st.sidebar.write(f"**👤 사용자**: {st.session_state.user[1]}")
    st.sidebar.write(f"**🏢 부서**: {st.session_state.user[4]}")
    st.sidebar.write(f"**📌 역할**: {'관리자' if st.session_state.role == 'admin' else '직원'}")

    st.sidebar.divider()

    # 네비게이션
    if st.session_state.role == 'admin':
        page = st.sidebar.radio(
            "메뉴",
            ["📈 대시보드", "📚 기본교육 관리", "✅ 자율교육 승인", "📊 통계 및 분석"]
        )

        if page == "📈 대시보드":
            st.write("관리자 대시보드 페이지입니다.")
            # TODO: 관리자 대시보드 구현

        elif page == "📚 기본교육 관리":
            st.write("기본교육 관리 페이지입니다.")
            # TODO: 기본교육 관리 구현

        elif page == "✅ 자율교육 승인":
            st.write("자율교육 승인 페이지입니다.")
            # TODO: 승인 관리 구현

        elif page == "📊 통계 및 분석":
            st.write("통계 및 분석 페이지입니다.")
            # TODO: 통계 구현

    else:  # employee
        page = st.sidebar.radio(
            "메뉴",
            ["📈 대시보드", "📚 기본교육 현황", "🎓 자율교육 관리"]
        )

        if page == "📈 대시보드":
            st.write("직원 대시보드 페이지입니다.")
            # TODO: 직원 대시보드 구현

        elif page == "📚 기본교육 현황":
            st.write("기본교육 현황 페이지입니다.")
            # TODO: 기본교육 현황 구현

        elif page == "🎓 자율교육 관리":
            st.write("자율교육 관리 페이지입니다.")
            # TODO: 자율교육 관리 구현
