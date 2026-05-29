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

# BMW 디자인 시스템 스타일
st.markdown("""
    <style>
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* 색상 시스템 */
    :root {
        --bmw-blue: #1c69d4;
        --bmw-blue-dark: #0653b6;
        --surface-dark: #1a2129;
        --surface-dark-elevated: #262e38;
        --canvas: #ffffff;
        --surface-card: #fafafa;
        --surface-soft: #f7f7f7;
        --surface-strong: #ebebeb;
        --hairline: #e6e6e6;
        --ink: #262626;
        --body: #3c3c3c;
        --muted: #6b6b6b;
        --on-dark: #ffffff;
    }

    /* 배경 */
    .main {
        background-color: var(--canvas);
        padding: 0;
    }

    /* 타이포그래피 */
    h1, h2, h3 {
        font-weight: 700;
        color: var(--ink);
        letter-spacing: 0;
    }

    p, span {
        font-weight: 300;
        color: var(--body);
    }

    /* 메트릭 카드 - 헤로 밴드 스타일 */
    .metric-hero {
        background-color: var(--surface-dark);
        color: var(--on-dark);
        padding: 80px 32px;
        margin: 0 0 80px 0;
        border-radius: 0;
    }

    .metric-hero h2 {
        color: var(--on-dark);
        margin: 0 0 40px 0;
        font-size: 48px;
    }

    /* 카드 */
    .card {
        background-color: var(--canvas);
        border: 1px solid var(--hairline);
        padding: 24px;
        margin-bottom: 24px;
        border-radius: 0;
    }

    .card-light {
        background-color: var(--surface-card);
        border: none;
    }

    /* 버튼 - BMW 스타일 */
    .stButton > button {
        background-color: var(--bmw-blue);
        color: white;
        border-radius: 0;
        padding: 14px 32px;
        height: 48px;
        font-weight: 700;
        border: none;
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    .stButton > button:hover {
        background-color: var(--bmw-blue-dark);
    }

    /* 섹션 스페이싱 */
    .section {
        margin-top: 80px;
        margin-bottom: 80px;
    }

    .section-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        color: var(--ink);
    }

    /* 테이블 */
    .dataframe {
        border-collapse: collapse;
    }

    .dataframe td, .dataframe th {
        border: 1px solid var(--hairline);
        padding: 12px;
        text-align: left;
        font-size: 14px;
    }

    .dataframe th {
        background-color: var(--surface-soft);
        font-weight: 700;
        color: var(--ink);
    }

    .dataframe tr:nth-child(even) {
        background-color: var(--canvas);
    }

    /* 입력 필드 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 0;
        border: 1px solid var(--hairline);
        font-size: 14px;
    }

    /* 헤더 */
    .header {
        background-color: var(--canvas);
        padding: 24px 32px;
        border-bottom: 1px solid var(--hairline);
        margin-bottom: 40px;
    }

    .header h1 {
        margin: 0;
        font-size: 48px;
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

# CSV 데이터 임포트
def import_csv_data(csv_file):
    """CSV 파일에서 교육 데이터 임포트"""
    try:
        # 인코딩 시도 순서
        for encoding in ['utf-8-sig', 'euc-kr', 'cp949', 'utf-8']:
            try:
                df = pd.read_csv(csv_file, encoding=encoding)
                break
            except:
                continue

        if df is None:
            return False, "CSV 파일을 읽을 수 없습니다."

        # 컬럼 정리 (첫 번째 행이 헤더일 가능성)
        if '직원번호' not in df.columns and df.iloc[0, 0] == '직원번호':
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

        conn = init_db()
        c = conn.cursor()

        imported_count = 0

        # 데이터 임포트
        for _, row in df.iterrows():
            try:
                # 사용자 추가 (직번과 성명으로)
                if pd.notna(row.get('직원번호')) and pd.notna(row.get('성명')):
                    user_id = str(row['직원번호']).strip()
                    name = str(row['성명']).strip().split('/')[0]  # "성명/직번" 형식 처리

                    c.execute('INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)',
                             (user_id, name, hashlib.sha256(user_id.encode()).hexdigest(), 'employee', ''))

                    # 기본교육 기록 추가
                    if pd.notna(row.get('교육명')) and row.get('교육분야') != '자율교육':
                        training_name = str(row['교육명']).strip()
                        status = 'completed' if row.get('교육이수여부') == '이수' else 'pending'
                        score = 0

                        # 점수 처리
                        try:
                            score_val = row.get('교육점수', 0)
                            if pd.notna(score_val):
                                score = int(score_val)
                        except:
                            pass

                        # 교육 ID 찾기 또는 생성
                        c.execute('SELECT id FROM mandatory_training WHERE training_name = ?', (training_name,))
                        result = c.fetchone()

                        if result:
                            training_id = result[0]
                            c.execute('INSERT OR IGNORE INTO mandatory_records (user_id, training_id, status, score) VALUES (?, ?, ?, ?)',
                                     (user_id, training_id, status, score))
                        else:
                            # 새 교육 생성
                            c.execute('INSERT INTO mandatory_training (training_name, description, year) VALUES (?, ?, ?)',
                                     (training_name, '', 2024))
                            c.execute('INSERT INTO mandatory_records (user_id, training_id, status, score) VALUES (?, last_insert_rowid(), ?, ?)',
                                     (user_id, status, score))

                    # 자율교육 기록 추가
                    elif pd.notna(row.get('교육명')) and row.get('교육분야') == '자율교육':
                        training_name = str(row['교육명']).strip()
                        provider = str(row.get('교육기관', '')).strip()

                        c.execute('INSERT INTO autonomous_training (user_id, training_name, provider, training_date, status, submitted_date) VALUES (?, ?, ?, ?, ?, ?)',
                                 (user_id, training_name, provider, datetime.now().strftime('%Y-%m-%d'), 'approved', datetime.now().strftime('%Y-%m-%d')))

                    imported_count += 1
            except Exception as e:
                continue

        conn.commit()
        conn.close()

        return True, f"✅ {imported_count}개의 교육 기록이 임포트되었습니다!"

    except Exception as e:
        return False, f"❌ 오류 발생: {str(e)}"

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
    # 로그인 페이지 - BMW 디자인
    create_sample_data()

    # 헤로 밴드
    st.markdown("""
        <div class="metric-hero">
            <h2>📚 교육 대시보드</h2>
            <p style="color: #bbbbbb; font-size: 16px; margin: 0;">직원 교육참여 실적 관리 시스템</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="card card-light">
                <h3 style="margin-top: 0; font-size: 18px;">👤 테스트 계정</h3>
                <p><strong>관리자</strong><br>직번: 001 / 비번: 001</p>
                <p><strong>직원</strong><br>직번: 002~004 / 비번: 002~004</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card card-light">
                <h3 style="margin-top: 0; font-size: 18px;">⚠️ 안내</h3>
                <p>초기 비밀번호는 직번과 동일합니다.</p>
                <p>로그인 후 비밀번호를 변경할 수 있습니다.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # 로그인 폼
    with st.form("login_form"):
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 30px;'>로그인</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            user_id = st.text_input("직번", placeholder="직번을 입력하세요", label_visibility="collapsed")

        with col2:
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요", label_visibility="collapsed")

        submitted = st.form_submit_button("로그인", use_container_width=True)

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
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>📈 관리자 대시보드</h2>
                    <p style="color: #bbbbbb; margin: 0;">전사 교육 현황 한눈에 보기</p>
                </div>
            """, unsafe_allow_html=True)

            conn = init_db()
            c = conn.cursor()

            # 통계
            c.execute('SELECT COUNT(*) FROM users WHERE role = "employee"')
            total_employees = c.fetchone()[0]

            c.execute('SELECT COUNT(*) FROM mandatory_training')
            total_trainings = c.fetchone()[0]

            c.execute('SELECT COUNT(*) FROM mandatory_records WHERE status = "completed"')
            completed_records = c.fetchone()[0]

            c.execute('SELECT COUNT(*) FROM autonomous_training WHERE status = "pending"')
            pending_approvals = c.fetchone()[0]

            conn.close()

            # 메트릭 카드
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">전체 직원</p>
                        <h3 style="margin: 0; font-size: 32px; color: #1c69d4;">{total_employees}</h3>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">기본교육</p>
                        <h3 style="margin: 0; font-size: 32px; color: #1c69d4;">{total_trainings}</h3>
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">이수 기록</p>
                        <h3 style="margin: 0; font-size: 32px; color: #1c69d4;">{completed_records}</h3>
                    </div>
                """, unsafe_allow_html=True)

            with col4:
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">승인 대기</p>
                        <h3 style="margin: 0; font-size: 32px; color: #e22718;">{pending_approvals}</h3>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

            # 기본교육 이수 현황
            st.markdown("<h3 class='section-title'>기본교육 이수 현황</h3>", unsafe_allow_html=True)

            conn = init_db()
            c = conn.cursor()

            c.execute('''SELECT mt.training_name,
                         COUNT(CASE WHEN mr.status = "completed" THEN 1 END) as completed,
                         COUNT(CASE WHEN mr.status = "pending" THEN 1 END) as pending,
                         COUNT(mr.id) as total
                         FROM mandatory_training mt
                         LEFT JOIN mandatory_records mr ON mt.id = mr.training_id
                         GROUP BY mt.id, mt.training_name''')

            results = c.fetchall()
            conn.close()

            if results:
                data = []
                for row in results:
                    completion_rate = int((row[1] / row[3] * 100)) if row[3] > 0 else 0
                    data.append({
                        '교육명': row[0],
                        '이수': row[1],
                        '대기': row[2],
                        '전체': row[3],
                        '이수율': f"{completion_rate}%"
                    })

                df = pd.DataFrame(data)
                st.markdown("""
                    <style>
                    .dataframe-container {
                        border: 1px solid #e6e6e6;
                        border-radius: 0;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)

        elif page == "📚 기본교육 관리":
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>📚 기본교육 관리</h2>
                    <p style="color: #bbbbbb; margin: 0;">교육과정 생성 및 이수 현황 관리</p>
                </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["📋 교육 목록", "➕ 새 교육 등록", "📥 CSV 임포트"])

            with tab1:
                conn = init_db()
                c = conn.cursor()

                c.execute('SELECT id, training_name, description, year FROM mandatory_training')
                trainings = c.fetchall()
                conn.close()

                st.markdown("<h3 class='section-title'>현재 교육 목록</h3>", unsafe_allow_html=True)

                if trainings:
                    for training in trainings:
                        st.markdown(f"""
                            <div class="card">
                                <h4 style="margin: 0 0 8px 0; font-size: 16px;">{training[1]}</h4>
                                <p style="margin: 0 0 8px 0; color: #6b6b6b; font-size: 14px;">{training[2]}</p>
                                <p style="margin: 0; color: #9a9a9a; font-size: 12px;">📅 {training[3]}년</p>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("등록된 교육이 없습니다.")

            with tab2:
                st.markdown("<h3 class='section-title'>새 교육 등록</h3>", unsafe_allow_html=True)

                with st.form("add_training_form"):
                    name = st.text_input("교육명", placeholder="교육 이름을 입력하세요")
                    desc = st.text_area("설명", placeholder="교육 내용을 입력하세요", height=100)
                    year = st.number_input("연도", min_value=2020, value=2024)

                    submitted = st.form_submit_button("등록", use_container_width=True)

                    if submitted:
                        if name:
                            conn = init_db()
                            c = conn.cursor()
                            c.execute('INSERT INTO mandatory_training (training_name, description, year) VALUES (?, ?, ?)',
                                     (name, desc, year))
                            conn.commit()
                            conn.close()
                            st.success("✅ 교육이 등록되었습니다!")
                            st.rerun()
                        else:
                            st.error("교육명을 입력해주세요.")

            with tab3:
                st.markdown("<h3 class='section-title'>CSV 파일 임포트</h3>", unsafe_allow_html=True)

                st.markdown("""
                    <div class="card card-light">
                        <p style="margin: 0; color: #6b6b6b; font-size: 14px;">
                        <strong>지원 형식:</strong> CSV 파일<br>
                        <strong>필수 컬럼:</strong> 직원번호, 성명, 교육명, 교육분야<br>
                        <strong>기능:</strong> 직원 정보 및 기본/자율교육 데이터 일괄 임포트
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type=['csv'])

                if uploaded_file is not None:
                    if st.button("임포트", use_container_width=True):
                        with st.spinner("데이터를 임포트하고 있습니다..."):
                            success, message = import_csv_data(uploaded_file)

                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            with tab2:
                conn = init_db()
                c = conn.cursor()

                c.execute('SELECT id, training_name FROM mandatory_training')
                trainings = c.fetchall()

                c.execute('SELECT user_id, name FROM users WHERE role = "employee"')
                employees = c.fetchall()
                conn.close()

                if trainings and employees:
                    training_names = {t[0]: t[1] for t in trainings}
                    training_id = st.selectbox("교육 선택", [t[0] for t in trainings],
                                              format_func=lambda x: training_names[x])

                    st.write(f"**{training_names[training_id]}** 이수 현황 입력")

                    for emp_id, emp_name in employees:
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col1:
                            st.write(f"**{emp_name}**")
                        with col2:
                            status = st.selectbox(f"{emp_id} 상태", ["미이수", "이수", "불합격"], key=f"status_{emp_id}")
                        with col3:
                            if status == "이수":
                                score = st.number_input(f"{emp_id} 점수", min_value=0, max_value=100, key=f"score_{emp_id}")
                            else:
                                score = None

                    if st.button("저장"):
                        conn = init_db()
                        c = conn.cursor()

                        for emp_id, _ in employees:
                            status_map = {"미이수": "pending", "이수": "completed", "불합격": "failed"}
                            st.session_state

                        st.success("✅ 저장되었습니다!")

        elif page == "✅ 자율교육 승인":
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>✅ 자율교육 승인</h2>
                    <p style="color: #bbbbbb; margin: 0;">직원의 자율교육 신청을 검토하고 승인합니다</p>
                </div>
            """, unsafe_allow_html=True)

            conn = init_db()
            c = conn.cursor()

            c.execute('''SELECT a.id, a.user_id, a.training_name, a.provider, a.submitted_date, u.name
                         FROM autonomous_training a
                         JOIN users u ON a.user_id = u.user_id
                         WHERE a.status = "pending"
                         ORDER BY a.submitted_date ASC''')

            pending_trainings = c.fetchall()
            conn.close()

            if pending_trainings:
                st.markdown(f"""
                    <div class="card" style="background-color: #fff3cd; border-color: #ffc107;">
                        <p style="margin: 0; color: #856404; font-weight: 700;">⚠️ 승인 대기 중인 신청</p>
                        <p style="margin: 0; color: #856404; font-size: 20px; font-weight: 700;">{len(pending_trainings)}건</p>
                    </div>
                """, unsafe_allow_html=True)

                st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

                for training in pending_trainings:
                    with st.expander(f"📌 {training[2]} - {training[5]}", expanded=False):
                        col1, col2 = st.columns([1.5, 1])

                        with col1:
                            st.markdown(f"""
                                <div>
                                    <p style="margin: 0 0 12px 0;"><strong>신청자</strong><br>{training[5]}</p>
                                    <p style="margin: 0 0 12px 0;"><strong>교육명</strong><br>{training[2]}</p>
                                    <p style="margin: 0 0 12px 0;"><strong>교육 기관</strong><br>{training[3]}</p>
                                    <p style="margin: 0;"><strong>신청 날짜</strong><br>{training[4]}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        with col2:
                            approval = st.radio("결정", ["승인", "거절"], horizontal=False, key=f"approval_{training[0]}")

                            if approval == "거절":
                                reason = st.text_area("거절 사유", placeholder="거절 사유를 입력하세요", key=f"reason_{training[0]}", height=80)
                            else:
                                reason = None

                            if st.button("처리", key=f"process_{training[0]}", use_container_width=True):
                                conn = init_db()
                                c = conn.cursor()

                                status = "approved" if approval == "승인" else "rejected"
                                c.execute('UPDATE autonomous_training SET status = ? WHERE id = ?',
                                         (status, training[0]))
                                conn.commit()
                                conn.close()

                                st.success(f"✅ {approval}했습니다!")
                                st.rerun()
            else:
                st.markdown("""
                    <div class="card card-light">
                        <p style="margin: 0; text-align: center; color: #6b6b6b;">
                        ✨ 승인 대기 중인 신청이 없습니다.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        elif page == "📊 통계 및 분석":
            st.subheader("📊 통계 및 분석")

            conn = init_db()
            c = conn.cursor()

            st.write("**직원별 교육 현황**")

            c.execute('''SELECT u.name,
                         COUNT(CASE WHEN mr.status = "completed" THEN 1 END) as completed,
                         COUNT(mr.id) as total
                         FROM users u
                         LEFT JOIN mandatory_records mr ON u.user_id = mr.user_id
                         WHERE u.role = "employee"
                         GROUP BY u.user_id, u.name''')

            results = c.fetchall()
            conn.close()

            if results:
                df = pd.DataFrame(results, columns=['직원명', '이수', '전체'])
                df['이수율(%)'] = (df['이수'] / df['전체'].replace(0, 1) * 100).astype(int)
                st.dataframe(df, use_container_width=True)

            st.divider()
            st.write("**자율교육 현황**")

            conn = init_db()
            c = conn.cursor()
            c.execute('''SELECT status, COUNT(*)
                         FROM autonomous_training
                         GROUP BY status''')

            status_results = c.fetchall()
            conn.close()

            if status_results:
                status_map = {'pending': '대기', 'approved': '승인', 'rejected': '거절'}
                data = {status_map.get(s[0], s[0]): s[1] for s in status_results}

                col1, col2, col3 = st.columns(3)
                for status_name, count in data.items():
                    with col1 if list(data.keys()).index(status_name) == 0 else (col2 if list(data.keys()).index(status_name) == 1 else col3):
                        st.metric(status_name, count)

    else:  # employee
        page = st.sidebar.radio(
            "메뉴",
            ["📈 대시보드", "📚 기본교육 현황", "🎓 자율교육 관리"]
        )

        if page == "📈 대시보드":
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>📈 내 교육 현황</h2>
                    <p style="color: #bbbbbb; margin: 0;">개인의 교육 이수 현황을 확인하세요</p>
                </div>
            """, unsafe_allow_html=True)

            user_id = st.session_state.user[0]
            conn = init_db()
            c = conn.cursor()

            # 기본교육 현황
            c.execute('''SELECT COUNT(*),
                         COUNT(CASE WHEN status = "completed" THEN 1 END)
                         FROM mandatory_records WHERE user_id = ?''', (user_id,))

            total_mandatory, completed_mandatory = c.fetchone()

            # 자율교육 현황
            c.execute('''SELECT COUNT(*),
                         COUNT(CASE WHEN status = "approved" THEN 1 END)
                         FROM autonomous_training WHERE user_id = ?''', (user_id,))

            total_autonomous, approved_autonomous = c.fetchone()

            conn.close()

            col1, col2 = st.columns(2)

            with col1:
                completion_rate = int((completed_mandatory / total_mandatory * 100)) if total_mandatory > 0 else 0
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">기본교육</p>
                        <h3 style="margin: 0 0 8px 0; font-size: 28px; color: #1c69d4;">{completed_mandatory}/{total_mandatory if total_mandatory > 0 else 0}</h3>
                        <p style="margin: 0; color: #9a9a9a; font-size: 12px;">이수율 {completion_rate}%</p>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                approval_rate = int((approved_autonomous / total_autonomous * 100)) if total_autonomous > 0 else 0
                st.markdown(f"""
                    <div class="card">
                        <p style="margin: 0 0 10px 0; color: #6b6b6b; font-size: 12px; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 700;">자율교육</p>
                        <h3 style="margin: 0 0 8px 0; font-size: 28px; color: #1c69d4;">{approved_autonomous}/{total_autonomous if total_autonomous > 0 else 0}</h3>
                        <p style="margin: 0; color: #9a9a9a; font-size: 12px;">승인율 {approval_rate}%</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

            st.markdown("<h3 class='section-title'>최근 이수 현황</h3>", unsafe_allow_html=True)

            conn = init_db()
            c = conn.cursor()

            c.execute('''SELECT mt.training_name, mr.status, mr.score, mr.completion_date
                         FROM mandatory_records mr
                         JOIN mandatory_training mt ON mr.training_id = mt.id
                         WHERE mr.user_id = ?
                         ORDER BY mr.completion_date DESC LIMIT 5''', (user_id,))

            results = c.fetchall()
            conn.close()

            if results:
                status_map = {'completed': '✅ 이수', 'pending': '⏳ 대기', 'failed': '❌ 불합격'}
                status_color = {'completed': '#22c55e', 'pending': '#f59e0b', 'failed': '#dc2626'}

                for row in results:
                    status_key = row[1]
                    color = status_color.get(status_key, '#6b6b6b')
                    score_display = f"({row[2]}점)" if row[2] else ""

                    st.markdown(f"""
                        <div class="card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0; font-size: 16px;">{row[0]}</h4>
                                <span style="color: {color}; font-weight: 700;">{status_map.get(status_key, status_key)} {score_display}</span>
                            </div>
                            <p style="margin: 4px 0 0 0; color: #9a9a9a; font-size: 12px;">{row[3]}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("이수 현황이 없습니다.")

        elif page == "📚 기본교육 현황":
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>📚 기본교육 현황</h2>
                    <p style="color: #bbbbbb; margin: 0;">필수 교육의 이수 현황을 확인하세요</p>
                </div>
            """, unsafe_allow_html=True)

            user_id = st.session_state.user[0]
            conn = init_db()
            c = conn.cursor()

            c.execute('''SELECT mt.training_name, mt.description, mr.status, mr.score, mt.year
                         FROM mandatory_training mt
                         LEFT JOIN mandatory_records mr ON mt.id = mr.training_id AND mr.user_id = ?
                         ORDER BY mt.year DESC, mt.training_name''', (user_id,))

            results = c.fetchall()
            conn.close()

            if results:
                status_map = {'completed': '✅ 이수', 'pending': '⏳ 대기', 'failed': '❌ 불합격', None: '📋 미정'}
                status_color = {'completed': '#22c55e', 'pending': '#f59e0b', 'failed': '#dc2626', None: '#6b6b6b'}

                for row in results:
                    status_key = row[2]
                    color = status_color.get(status_key, '#6b6b6b')
                    score_display = f"({row[3]}점)" if row[3] else ""

                    st.markdown(f"""
                        <div class="card">
                            <div style="display: flex; justify-content: space-between; align-items: start;">
                                <div style="flex: 1;">
                                    <h4 style="margin: 0 0 8px 0; font-size: 16px;">{row[0]}</h4>
                                    <p style="margin: 0; color: #6b6b6b; font-size: 14px;">{row[1]}</p>
                                </div>
                                <div style="text-align: right;">
                                    <p style="margin: 0; color: {color}; font-weight: 700; font-size: 14px;">{status_map.get(status_key)} {score_display}</p>
                                    <p style="margin: 4px 0 0 0; color: #9a9a9a; font-size: 12px;">{row[4]}년</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="card card-light">
                        <p style="margin: 0; text-align: center; color: #6b6b6b;">
                        교육 정보가 없습니다.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        elif page == "🎓 자율교육 관리":
            # 헤로 밴드
            st.markdown("""
                <div class="metric-hero">
                    <h2>🎓 자율교육 관리</h2>
                    <p style="color: #bbbbbb; margin: 0;">자율교육 신청 및 현황을 관리하세요</p>
                </div>
            """, unsafe_allow_html=True)

            user_id = st.session_state.user[0]

            tab1, tab2 = st.tabs(["➕ 새로 신청", "📋 신청 현황"])

            with tab1:
                st.write("**자율교육 신청**")

                with st.form("autonomous_form"):
                    training_name = st.text_input("교육명")
                    provider = st.text_input("교육 기관")
                    training_date = st.date_input("교육 수료 날짜")
                    description = st.text_area("교육 내용 및 설명", height=100)
                    uploaded_file = st.file_uploader("증빙 파일 (선택)", type=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])

                    if st.form_submit_button("신청"):
                        if training_name and provider:
                            conn = init_db()
                            c = conn.cursor()

                            c.execute('''INSERT INTO autonomous_training
                                        (user_id, training_name, provider, training_date, description, status, submitted_date)
                                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                     (user_id, training_name, provider, str(training_date), description, 'pending', datetime.now().strftime('%Y-%m-%d')))

                            conn.commit()
                            conn.close()

                            st.success("✅ 자율교육이 신청되었습니다!")
                            st.info("관리자 승인을 기다려주세요.")
                            st.rerun()
                        else:
                            st.error("교육명과 기관을 입력해주세요.")

            with tab2:
                st.write("**신청 현황**")

                conn = init_db()
                c = conn.cursor()

                c.execute('''SELECT id, training_name, provider, training_date, status, submitted_date
                             FROM autonomous_training
                             WHERE user_id = ?
                             ORDER BY submitted_date DESC''', (user_id,))

                results = c.fetchall()
                conn.close()

                if results:
                    status_map = {'pending': '⏳ 승인 대기', 'approved': '✅ 승인됨', 'rejected': '❌ 거절됨'}

                    for row in results:
                        with st.expander(f"🔹 {row[1]} - {status_map.get(row[4], row[4])}"):
                            col1, col2 = st.columns(2)

                            with col1:
                                st.write(f"**교육 기관**: {row[2]}")
                                st.write(f"**수료 날짜**: {row[3]}")

                            with col2:
                                st.write(f"**신청 날짜**: {row[5]}")
                                st.write(f"**상태**: {status_map.get(row[4], row[4])}")

                            if row[4] == 'pending':
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("수정", key=f"edit_{row[0]}"):
                                        st.info("수정 기능은 추후 구현 예정입니다.")
                                with col2:
                                    if st.button("삭제", key=f"delete_{row[0]}"):
                                        conn = init_db()
                                        c = conn.cursor()
                                        c.execute('DELETE FROM autonomous_training WHERE id = ?', (row[0],))
                                        conn.commit()
                                        conn.close()
                                        st.success("✅ 삭제되었습니다!")
                                        st.rerun()
                else:
                    st.info("신청한 자율교육이 없습니다.")
