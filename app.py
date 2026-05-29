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
            st.subheader("📈 관리자 대시보드")

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

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("전체 직원", f"{total_employees}명")
            with col2:
                st.metric("기본교육", f"{total_trainings}개")
            with col3:
                st.metric("이수 기록", f"{completed_records}개")
            with col4:
                st.metric("승인 대기", f"{pending_approvals}건")

            st.divider()
            st.write("📚 기본교육 이수 현황")

            conn = init_db()
            c = conn.cursor()

            c.execute('''SELECT mt.training_name,
                         COUNT(CASE WHEN mr.status = "completed" THEN 1 END) as completed,
                         COUNT(CASE WHEN mr.status = "pending" THEN 1 END) as pending
                         FROM mandatory_training mt
                         LEFT JOIN mandatory_records mr ON mt.id = mr.training_id
                         GROUP BY mt.id, mt.training_name''')

            results = c.fetchall()
            conn.close()

            if results:
                df = pd.DataFrame(results, columns=['교육명', '이수', '대기'])
                st.dataframe(df, use_container_width=True)

        elif page == "📚 기본교육 관리":
            st.subheader("📚 기본교육 관리")

            tab1, tab2 = st.tabs(["교육 관리", "이수 현황 입력"])

            with tab1:
                conn = init_db()
                c = conn.cursor()

                c.execute('SELECT id, training_name, description, year FROM mandatory_training')
                trainings = c.fetchall()
                conn.close()

                st.write("**현재 교육 목록**")
                if trainings:
                    for training in trainings:
                        col1, col2, col3 = st.columns([2, 3, 1])
                        with col1:
                            st.write(f"**{training[1]}**")
                        with col2:
                            st.write(f"📄 {training[2]}")
                        with col3:
                            st.write(f"📅 {training[3]}")

                st.divider()
                st.write("**새 교육 등록**")

                with st.form("add_training_form"):
                    name = st.text_input("교육명")
                    desc = st.text_area("설명", height=100)
                    year = st.number_input("연도", min_value=2020, value=2024)

                    if st.form_submit_button("등록"):
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
            st.subheader("✅ 자율교육 승인")

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
                st.write(f"**대기 중인 신청: {len(pending_trainings)}건**")

                for training in pending_trainings:
                    with st.expander(f"🔹 {training[2]} - {training[5]} ({training[4]})"):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.write(f"**신청자**: {training[5]}")
                            st.write(f"**교육명**: {training[2]}")
                            st.write(f"**기관**: {training[3]}")

                        with col2:
                            approval = st.radio("결정", ["승인", "거절"], horizontal=True, key=f"approval_{training[0]}")

                            if approval == "거절":
                                reason = st.text_area("거절 사유", key=f"reason_{training[0]}")
                            else:
                                reason = None

                            if st.button("처리", key=f"process_{training[0]}"):
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
                st.info("승인 대기 중인 신청이 없습니다.")

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
            st.subheader("📈 내 교육 현황")

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
                st.metric("기본교육", f"{completed_mandatory}/{total_mandatory if total_mandatory > 0 else 0}")

            with col2:
                st.metric("자율교육 (승인됨)", f"{approved_autonomous}/{total_autonomous if total_autonomous > 0 else 0}")

            st.divider()
            st.write("📚 최근 기본교육 현황")

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

                for row in results:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**{row[0]}**")
                    with col2:
                        st.write(status_map.get(row[1], row[1]))
                    with col3:
                        if row[2]:
                            st.write(f"📊 {row[2]}점")

        elif page == "📚 기본교육 현황":
            st.subheader("📚 기본교육 현황")

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

                data = []
                for row in results:
                    status_display = status_map.get(row[2], row[2])
                    score = f"{row[3]}점" if row[3] else "-"
                    data.append({
                        '교육명': row[0],
                        '상태': status_display,
                        '점수': score,
                        '연도': row[4]
                    })

                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("교육 정보가 없습니다.")

        elif page == "🎓 자율교육 관리":
            st.subheader("🎓 자율교육 관리")

            user_id = st.session_state.user[0]

            tab1, tab2 = st.tabs(["신청", "현황"])

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
