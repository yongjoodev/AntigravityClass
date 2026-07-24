import random
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="숫자 맞추기 게임 | Number Guessing Game",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Aesthetics
st.markdown(
    """
    <style>
    /* Main container background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
        color: #f8fafc;
    }
    
    /* Header Card */
    .main-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    .main-header h1 {
        background: linear-gradient(90deg, #38bdf8, #a855f7, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #cbd5e1;
        font-size: 1.1rem;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Badge & Tag Styles */
    .badge-up {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .badge-down {
        background-color: #3b82f6;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }

    .badge-success {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def init_game():
    """Initialize or reset session state variables."""
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.min_range = 1
    st.session_state.max_range = 100
    st.session_state.game_over = False
    st.session_state.message = None
    st.session_state.message_type = None


# Session State Initialization
if "target_number" not in st.session_state:
    init_game()

if "best_score" not in st.session_state:
    st.session_state.best_score = None


def handle_guess():
    """Process user's guess."""
    guess = st.session_state.user_guess

    if guess < 1 or guess > 100:
        st.session_state.message = "⚠️ 1부터 100 사이의 숫자를 입력해주세요."
        st.session_state.message_type = "warning"
        return

    st.session_state.attempts += 1

    if guess < st.session_state.target_number:
        st.session_state.min_range = max(st.session_state.min_range, guess + 1)
        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": guess,
                "result": "UP ⬆️",
                "detail": "더 큰 숫자를 입력하세요!",
            }
        )
        st.session_state.message = f"⬆️ UP! {guess}보다 큰 숫자입니다."
        st.session_state.message_type = "error"

    elif guess > st.session_state.target_number:
        st.session_state.max_range = min(st.session_state.max_range, guess - 1)
        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": guess,
                "result": "DOWN ⬇️",
                "detail": "더 작은 숫자를 입력하세요!",
            }
        )
        st.session_state.message = f"⬇️ DOWN! {guess}보다 작은 숫자입니다."
        st.session_state.message_type = "info"

    else:
        st.session_state.game_over = True
        st.session_state.history.append(
            {
                "attempt": st.session_state.attempts,
                "guess": guess,
                "result": "CORRECT 🎉",
                "detail": "정답입니다!",
            }
        )
        st.session_state.message = (
            f"🎉 정답입니다! ({st.session_state.target_number})"
        )
        st.session_state.message_type = "success"

        # Update best score
        if (
            st.session_state.best_score is None
            or st.session_state.attempts < st.session_state.best_score
        ):
            st.session_state.best_score = st.session_state.attempts


# --- UI Layout ---

# Sidebar Controls & Information
with st.sidebar:
    st.title("⚙️ 게임 설정 & 정보")
    st.info("💡 **게임 규칙**\n\n1~100 사이의 숫자를 최소한의 시도 횟수로 맞춰보세요!")

    if st.session_state.best_score is not None:
        st.success(
            f"🏆 **최고 기록**: {st.session_state.best_score}회 성공"
        )
    else:
        st.write("🏆 **최고 기록**: 아직 기록 없음")

    st.markdown("---")

    if st.button("🔄 새 게임 시작", use_container_width=True):
        init_game()
        st.rerun()

    st.markdown("---")
    st.caption("Developed with Streamlit & Python 🐍")


# Header Section
st.markdown(
    """
    <div class="main-header">
        <h1>🎯 1 to 100 숫자 맞추기 게임</h1>
        <p>비밀 숫자를 맞춰보세요! 시도 횟수가 적을수록 높은 점수를 얻습니다.</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Top Metrics Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 현재 시도 횟수", value=f"{st.session_state.attempts} 회")
with col2:
    st.metric(
        label="🔍 추정 범위",
        value=f"{st.session_state.min_range} ~ {st.session_state.max_range}",
    )
with col3:
    best_display = (
        f"{st.session_state.best_score} 회"
        if st.session_state.best_score
        else "-"
    )
    st.metric(label="🏆 최고 기록", value=best_display)

st.markdown("<br>", unsafe_allow_html=True)

# Main Game Area
if not st.session_state.game_over:
    st.subheader("🎲 숫자를 입력하세요")

    # Form to handle submit nicely
    with st.form(key="guess_form", clear_on_submit=True):
        col_input, col_btn = st.columns([3, 1])

        with col_input:
            user_guess = st.number_input(
                "1부터 100 사이의 숫자",
                min_value=1,
                max_value=100,
                step=1,
                key="user_guess",
                label_visibility="collapsed",
            )

        with col_btn:
            submit_button = st.form_submit_button(
                label="제출 🚀",
                use_container_width=True,
                on_click=handle_guess,
            )

    # Feedback Messages
    if st.session_state.message:
        if st.session_state.message_type == "warning":
            st.warning(st.session_state.message)
        elif st.session_state.message_type == "error":
            st.error(st.session_state.message)
        elif st.session_state.message_type == "info":
            st.info(st.session_state.message)

else:
    # Game Over / Victory Section
    st.balloons()
    st.success(
        f"🎊 **축하합니다!** {st.session_state.attempts}회 만에 정답 **{st.session_state.target_number}**를 맞추셨습니다!"
    )

    col_replay, col_empty = st.columns([1, 1])
    with col_replay:
        if st.button(
            "🔄 다시 도전하기", type="primary", use_container_width=True
        ):
            init_game()
            st.rerun()

# History Section
if st.session_state.history:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.subheader("📜 시도 기록")

    # Display history in reverse chronological order
    for item in reversed(st.session_state.history):
        cols = st.columns([1, 2, 2])
        with cols[0]:
            st.write(f"**{item['attempt']}회차**")
        with cols[1]:
            st.write(f"입력값: `{item['guess']}`")
        with cols[2]:
            if "UP" in item["result"]:
                st.markdown(
                    f"<span class='badge-up'>{item['result']}</span>",
                    unsafe_allow_html=True,
                )
            elif "DOWN" in item["result"]:
                st.markdown(
                    f"<span class='badge-down'>{item['result']}</span>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<span class='badge-success'>{item['result']}</span>",
                    unsafe_allow_html=True,
                )
