import streamlit as st
import numpy as np

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Tic Tac Toe",
    page_icon="🎮",
    layout="centered"
)


# ---------------- INITIALIZE GAME ----------------

if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)

if "current" not in st.session_state:
    st.session_state.current = 1

if "result" not in st.session_state:
    st.session_state.result = None

if "celebrated" not in st.session_state:
    st.session_state.celebrated = False

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* Animated background */

.stApp {
    background: linear-gradient(
        -45deg,
        #141e30,
        #243b55,
        #42275a,
        #141e30
    );

    background-size: 400% 400%;
    animation: backgroundMove 12s ease infinite;
}

@keyframes backgroundMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}


/* Heading */

h1 {
    color: white !important;
    text-align: center;
    text-shadow: 0 0 15px #00d4ff;
    font-size: 45px !important;
}

h2, h3, p {
    color: white !important;
}


/* Game buttons */

.stButton > button {
    height: 100px;
    width: 100%;
    font-size: 35px;
    font-weight: bold;

    background: rgba(255,255,255,0.12);
    color: white;

    border: 2px solid #00d4ff;
    border-radius: 18px;

    transition: all 0.3s ease;
}


/* Hover animation */

.stButton > button:hover:not(:disabled) {
    background: rgba(0,212,255,0.3);
    transform: scale(1.05);
    box-shadow: 0 0 20px #00d4ff;
    border-color: white;
}


/* Played cells */

.stButton > button:disabled {
    opacity: 1;
    color: white;
    background: rgba(255,255,255,0.15);
}


/* Restart button */

div[data-testid="stButton"]:last-child button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border: none;
    border-radius: 30px;
}


/* Welcome curtain animation */

.curtain-container {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;

    display: flex;
    z-index: 999999;

    pointer-events: none;

    animation: hideCurtain 0.1s 2.6s forwards;
}

.curtain {
    width: 50%;
    height: 100%;
    background: linear-gradient(
        135deg,
        #090979,
        #3a0ca3,
        #7209b7
    );

    box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
}

.left-curtain {
    animation: openLeft 2.5s ease-in-out forwards;
}

.right-curtain {
    animation: openRight 2.5s ease-in-out forwards;
}

@keyframes openLeft {
    to {
        transform: translateX(-100%);
    }
}

@keyframes openRight {
    to {
        transform: translateX(100%);
    }
}


/* Welcome text */

.welcome-text {
    position: absolute;
    top: 42%;
    left: 0;
    width: 100%;

    text-align: center;
    color: white;

    font-size: 35px;
    font-weight: bold;

    text-shadow: 0 0 20px #00d4ff;

    animation: welcomeFade 2.2s ease forwards;
}

@keyframes welcomeFade {
    0% {
        opacity: 0;
        transform: scale(0.5);
    }

    40% {
        opacity: 1;
        transform: scale(1.1);
    }

    75% {
        opacity: 1;
    }

    100% {
        opacity: 0;
        transform: scale(1.4);
    }
}

@keyframes hideCurtain {
    to {
        visibility: hidden;
    }
}

</style>
""", unsafe_allow_html=True)


# ---------------- WELCOME ANIMATION ----------------

if not st.session_state.welcome_shown:

    st.html("""
        <div class="curtain-container">
            <div class="curtain left-curtain"></div>
            <div class="curtain right-curtain"></div>

            <div class="welcome-text">
                🎮 WELCOME TO TIC TAC TOE
            </div>
        </div>
    """)

    st.session_state.welcome_shown = True


# ---------------- CHECK WINNER ----------------

def check_winner(b):

    # Check rows

    if 3 in np.sum(b, axis=1):
        return "X"

    if -3 in np.sum(b, axis=1):
        return "O"

    # Check columns

    if 3 in np.sum(b, axis=0):
        return "X"

    if -3 in np.sum(b, axis=0):
        return "O"

    # Check diagonals

    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return "X"

    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return "O"

    # Check draw

    if not np.any(b == 0):
        return "Draw"

    return None


# ---------------- MAKE MOVE ----------------

def make_move(row, col):

    if st.session_state.board[row, col] == 0:

        st.session_state.board[row, col] = st.session_state.current

        st.session_state.result = check_winner(
            st.session_state.board
        )

        if st.session_state.result is None:
            st.session_state.current *= -1


# ---------------- RESTART GAME ----------------

def restart_game():

    st.session_state.board = np.zeros((3, 3), dtype=int)

    st.session_state.current = 1

    st.session_state.result = None

    st.session_state.celebrated = False
    
    
# ---------------- RESULT POPUP ----------------

@st.dialog("🎮 GAME OVER!", width="large")
def show_result():

    result = st.session_state.result

    if result == "X":

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #11998e, #38ef7d);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 0 25px rgba(56,239,125,0.5);
        ">
            <div style="font-size: 75px;">🏆</div>
            <h1 style="color:white !important; font-size:35px;">
                PLAYER X WINS!
            </h1>
            <h2 style="color:white !important;">
                🎉 Congratulations! 🎉
            </h2>
            <p style="color:white !important;">
                Amazing performance! You are the champion!
            </p>
            <div style="font-size:35px;">🥳 🎊 🏅</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.celebrated:
            st.balloons()
            st.session_state.celebrated = True

    elif result == "O":

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #654ea3, #eaafc8);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 0 25px rgba(234,175,200,0.5);
        ">
            <div style="font-size: 75px;">🏆</div>
            <h1 style="color:white !important; font-size:35px;">
                PLAYER O WINS!
            </h1>
            <h2 style="color:white !important;">
                🎊 Fantastic Victory! 🎊
            </h2>
            <p style="color:white !important;">
                Brilliant moves! You nailed it!
            </p>
            <div style="font-size:35px;">🥳 🎉 🥇</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.celebrated:
            st.balloons()
            st.session_state.celebrated = True

    elif result == "Draw":

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #396afc, #2948ff);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 0 25px rgba(57,106,252,0.5);
        ">
            <div style="font-size: 75px;">🤝</div>
            <h1 style="color:white !important; font-size:35px;">
                IT'S A DRAW!
            </h1>
            <h2 style="color:white !important;">
                😍 WELL PLAYED!
            </h2>
            <p style="color:white !important;">
                Both players gave their best!
            </p>
            <div style="font-size:35px;">👏 🎉 💫</div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.celebrated:
            st.snow()
            st.session_state.celebrated = True

    st.write("")
    if st.button(
        "🔄 PLAY AGAIN",
        key="popup_play_again",
        use_container_width=True
    ):
        restart_game()
        st.rerun()



# ---------------- GAME INTERFACE ----------------

st.title("🎮 TIC TAC TOE")

st.markdown(
    "<p style='text-align:center;'>"
    "Two Players • One Board • One Winner"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- PLAYER TURN ----------------

if st.session_state.result is None:

    player = "X" if st.session_state.current == 1 else "O"

    st.subheader(f"🎯 Player {player}'s Turn")

else:

    show_result()



# ---------------- GAME BOARD ----------------

symbols = {
    0: " ",
    1: "❌",
    -1: "⭕"
}

for r in range(3):

    cols = st.columns(3)

    for c in range(3):

        value = st.session_state.board[r, c]

        cols[c].button(
            symbols[value],
            key=f"cell_{r}_{c}",
            use_container_width=True,

            disabled=(
                value != 0 or
                st.session_state.result is not None
            ),

            on_click=make_move,
            args=(r, c)
        )


st.divider()


# Restart button
st.button(
    "🔄 Restart Game",
    on_click=restart_game,
    use_container_width=True
)


