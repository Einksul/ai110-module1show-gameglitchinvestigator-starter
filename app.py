import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")


if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "message" not in st.session_state:
    st.session_state.message = None

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

#FIX: changing the difficulty now restarts the game
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.message = None

st.subheader("Make a guess")

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

#FIX: handle the logic before we render data! So we don't render stale data
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.message = None
    st.session_state.secret = random.randint(low, high)

just_finished = False

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.session_state.message = ("error", err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            just_finished = True
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            just_finished = True
        else:
            st.session_state.message = ("hint", message)

# --- Display (all state is now up-to-date) ---
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(attempt_limit - st.session_state.attempts, 0)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

if st.session_state.message:
    msg_type, msg_text = st.session_state.message
    if msg_type == "error":
        st.error(msg_text)
    elif msg_type == "hint" and show_hint:
        st.warning(msg_text)
    st.session_state.message = None

if st.session_state.status == "won":
    if just_finished:
        st.balloons()
        st.success(
            f"You won! The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}"
        )
    else:
        st.success("You already won. Start a new game to play again.")
elif st.session_state.status == "lost":
    if just_finished:
        st.error(
            f"Out of attempts! The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}"
        )
    else:
        st.error("Game over. Start a new game to try again.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
