```python
from flask import Flask, render_template, request, redirect, url_for
from database.database import load_player, save_player
from game.adaptive_engine import AdaptiveEngine
from game.logic import QUESTIONS
from game.scoring import calculate_performance, calculate_points
import time
import random

app = Flask(__name__)

# Temporary game data for the current browser session
game_state = {}


# -----------------------------------------
# HOME / DASHBOARD
# -----------------------------------------

@app.route("/")
def home():

    player = load_player()

    return render_template(
        "index.html",
        player=player
    )


# -----------------------------------------
# START CHALLENGE
# -----------------------------------------

@app.route("/start")
def start():

    player = load_player()

    engine = AdaptiveEngine()

    # Choose unassessed skill first,
    # otherwise choose weakest skill.
    skill = engine.choose_skill(player["skills"])

    # Currently Logic has questions.
    # Other skills can be added later.
    if skill != "Logic":
        skill = "Logic"

    difficulty = engine.choose_difficulty(
        player["skills"][skill]
    )

    questions = QUESTIONS[difficulty].copy()

    random.shuffle(questions)

    # Store game information
    game_state.clear()

    game_state["skill"] = skill
    game_state["difficulty"] = difficulty
    game_state["questions"] = questions
    game_state["current"] = 0
    game_state["correct"] = 0
    game_state["total_performance"] = 0
    game_state["total_points"] = 0
    game_state["start_time"] = time.time()

    return redirect(url_for("challenge"))


# -----------------------------------------
# CHALLENGE
# -----------------------------------------

@app.route("/challenge", methods=["GET", "POST"])
def challenge():

    if "questions" not in game_state:
        return redirect(url_for("home"))

    questions = game_state["questions"]
    current = game_state["current"]

    # -------------------------------------
    # PROCESS ANSWER
    # -------------------------------------

    if request.method == "POST":

        answer = request.form.get("answer", "").strip()

        question, correct_answer, target_time = questions[current]

        start_time = game_state["start_time"]

        elapsed = time.time() - start_time

        correct = answer == correct_answer

        performance = calculate_performance(
            correct,
            elapsed,
            game_state["difficulty"]
            if False
            else target_time
        )

        points = calculate_points(
            performance,
            game_state["difficulty"]
        )

        if correct:
            game_state["correct"] += 1

        game_state["total_performance"] += performance
        game_state["total_points"] += points

        # Move to next question
        game_state["current"] += 1

        # Reset timer
        game_state["start_time"] = time.time()

        # ---------------------------------
        # ROUND COMPLETE
        # ---------------------------------

        if game_state["current"] >= len(questions):

            return redirect(url_for("result"))

    # Current question
    question, correct_answer, target_time = questions[
        game_state["current"]
    ]

    return render_template(
        "game.html",
        skill=game_state["skill"],
        difficulty=game_state["difficulty"].capitalize(),
        question=question,
        question_number=game_state["current"] + 1,
        total_questions=len(questions)
    )


# -----------------------------------------
# RESULT
# -----------------------------------------

@app.route("/result")
def result():

    if "questions" not in game_state:
        return redirect(url_for("home"))

    player = load_player()

    total_questions = len(game_state["questions"])

    average_performance = round(
        game_state["total_performance"] / total_questions
    )

    correct_count = game_state["correct"]

    points = game_state["total_points"]

    skill = game_state["skill"]

    # -------------------------------------
    # UPDATE SKILL
    # -------------------------------------

    player["skills"][skill] = average_performance

    # -------------------------------------
    # UPDATE POINTS
    # -------------------------------------

    player["total_points"] += points

    # -------------------------------------
    # UPDATE GAMES
    # -------------------------------------

    player["games_played"] += 1

    # -------------------------------------
    # UPDATE STREAK
    # -------------------------------------

    if correct_count == total_questions:
        player["streak"] += 1

    else:
        player["streak"] = 0

    # Best streak
    if player["streak"] > player["best_streak"]:
        player["best_streak"] = player["streak"]

    # -------------------------------------
    # BADGES
    # -------------------------------------

    badges = player["badges"]

    if player["games_played"] >= 1:
        if "First Challenge" not in badges:
            badges.append("First Challenge")

    if player["streak"] >= 3:
        if "3 Day Streak" not in badges:
            badges.append("3 Challenge Streak")

    if player["total_points"] >= 100:
        if "100 Points" not in badges:
            badges.append("100 Points")

    if average_performance >= 90:
        if "Sharp Mind" not in badges:
            badges.append("Sharp Mind")

    # -------------------------------------
    # SAVE
    # -------------------------------------

    save_player(player)

    result_data = {
        "skill": skill,
        "difficulty": game_state["difficulty"],
        "correct": correct_count,
        "total": total_questions,
        "performance": average_performance,
        "points": points
    }

    # Clear current game
    game_state.clear()

    return render_template(
        "result.html",
        result=result_data,
        player=player
    )


# -----------------------------------------
# RUN SERVER
# -----------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
```
