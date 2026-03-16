from logic_utils import check_guess, get_range_for_difficulty, update_score

# --- check_guess tests ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- difficulty bounds tests ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_unknown_difficulty_defaults_to_hard():
    low, high = get_range_for_difficulty("Unknown")
    assert low == 1
    assert high == 100


# --- difficulty change resets game state ---

def test_difficulty_change_resets_state():
    """Simulate the reset logic from app.py when difficulty changes."""
    # Start with a game in progress on Normal
    state = {
        "difficulty": "Normal",
        "attempts": 3,
        "score": 85,
        "status": "playing",
        "history": [30, 40, 45],
        "message": ("hint", "Go HIGHER!"),
    }

    new_difficulty = "Hard"

    # This mirrors the reset block in app.py (lines 52-60)
    if state["difficulty"] != new_difficulty:
        state["difficulty"] = new_difficulty
        state["attempts"] = 0
        state["score"] = 0
        state["status"] = "playing"
        state["history"] = []
        state["message"] = None

    assert state["difficulty"] == "Hard"
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []
    assert state["message"] is None

def test_same_difficulty_does_not_reset():
    """State should be untouched when difficulty hasn't changed."""
    state = {
        "difficulty": "Normal",
        "attempts": 3,
        "score": 85,
        "status": "playing",
        "history": [30, 40, 45],
        "message": ("hint", "Go HIGHER!"),
    }

    new_difficulty = "Normal"

    if state["difficulty"] != new_difficulty:
        state["attempts"] = 0

    # Nothing should have changed
    assert state["attempts"] == 3
    assert state["score"] == 85


# --- score decrement on incorrect guess ---

def test_score_decrements_by_5_on_too_high():
    new_score = update_score(100, "Too High", 1)
    assert new_score == 95

def test_score_decrements_by_5_on_too_low():
    new_score = update_score(100, "Too Low", 1)
    assert new_score == 95

def test_score_decrements_accumulate():
    """Multiple wrong guesses should each subtract 5."""
    score = 100
    score = update_score(score, "Too High", 1)
    score = update_score(score, "Too Low", 2)
    score = update_score(score, "Too High", 3)
    assert score == 85

def test_score_can_go_negative():
    new_score = update_score(0, "Too Low", 1)
    assert new_score == -5


# --- game state transitions on win/loss ---

def test_state_changes_to_won_on_correct_guess():
    """Simulate the game loop: correct guess sets status to 'won'."""
    state = {"status": "playing", "attempts": 0, "score": 0}
    secret = 42
    guess = 42
    attempt_limit = 6

    state["attempts"] += 1
    outcome, message = check_guess(guess, secret)
    state["score"] = update_score(state["score"], outcome, state["attempts"])

    if outcome == "Win":
        state["status"] = "won"
    elif state["attempts"] >= attempt_limit:
        state["status"] = "lost"

    assert state["status"] == "won"
    assert state["score"] > 0

def test_state_changes_to_lost_when_attempts_exhausted():
    """Simulate the game loop: using all attempts sets status to 'lost'."""
    state = {"status": "playing", "attempts": 0, "score": 0}
    secret = 42
    attempt_limit = 3

    wrong_guesses = [10, 20, 30]
    for guess in wrong_guesses:
        state["attempts"] += 1
        outcome, message = check_guess(guess, secret)
        state["score"] = update_score(state["score"], outcome, state["attempts"])

        if outcome == "Win":
            state["status"] = "won"
        elif state["attempts"] >= attempt_limit:
            state["status"] = "lost"

    assert state["status"] == "lost"
    assert state["attempts"] == attempt_limit
    assert state["score"] == -15  # 3 wrong guesses * -5

def test_state_stays_playing_with_attempts_remaining():
    """Wrong guess with attempts left keeps status as 'playing'."""
    state = {"status": "playing", "attempts": 0, "score": 0}
    secret = 42
    attempt_limit = 6

    state["attempts"] += 1
    outcome, message = check_guess(10, secret)
    state["score"] = update_score(state["score"], outcome, state["attempts"])

    if outcome == "Win":
        state["status"] = "won"
    elif state["attempts"] >= attempt_limit:
        state["status"] = "lost"

    assert state["status"] == "playing"
    assert state["attempts"] == 1
