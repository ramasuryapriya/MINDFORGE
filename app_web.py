
from flask import Flask, render_template, request, redirect, url_for

from database.database import load_player, save_player

from game.adaptive_engine import AdaptiveEngine

from game.logic import QUESTIONS as LOGIC_QUESTIONS
from game.pattern import QUESTIONS as PATTERN_QUESTIONS
from game.memory import QUESTIONS as MEMORY_QUESTIONS
from game.strategy import QUESTIONS as STRATEGY_QUESTIONS
from game.attention import QUESTIONS as ATTENTION_QUESTIONS

from game.scoring import calculate_performance, calculate_points

import time
import random


app = Flask(__name__)


# =====================================================
# ALL GAMES
# =====================================================

GAME_QUESTIONS = {

    "Logic": LOGIC_QUESTIONS,

    "Pattern Recognition": PATTERN_QUESTIONS,

    "Memory": MEMORY_QUESTIONS,

    "Strategy": STRATEGY_QUESTIONS,

    "Attention": ATTENTION_QUESTIONS

}


# =====================================================
# CURRENT GAME
# =====================================================

game_state = {}


# =====================================================
# HOME
# =====================================================

@app.route("/")
def home():

    player = load_player()

    return render_template(
        "index.html",
        player=player
    )


# =====================================================
# START SPECIFIC SKILL
# =====================================================

@app.route("/start/<skill>")
def start_skill(skill):

    if skill not in GAME_QUESTIONS:

        return redirect(
            url_for("home")
        )


    player = load_player()

    engine = AdaptiveEngine()


    difficulty = engine.choose_difficulty(
        player["skills"][skill]
    )


    questions = GAME_QUESTIONS[skill][difficulty].copy()

    random.shuffle(questions)


    game_state.clear()


    game_state["skill"] = skill

    game_state["difficulty"] = difficulty

    game_state["questions"] = questions

    game_state["current"] = 0

    game_state["correct"] = 0

    game_state["total_performance"] = 0

    game_state["total_points"] = 0

    game_state["start_time"] = time.time()


    return redirect(
        url_for("challenge")
    )


# =====================================================
# ADAPTIVE START
# =====================================================

@app.route("/start")
def start():

    player = load_player()

    engine = AdaptiveEngine()


    skill = engine.choose_skill(
        player["skills"]
    )


    return redirect(
        url_for(
            "start_skill",
            skill=skill
        )
    )


# =====================================================
# CHALLENGE
# =====================================================

@app.route("/challenge", methods=["GET", "POST"])
def challenge():

    if "questions" not in game_state:

        return redirect(
            url_for("home")
        )


    questions = game_state["questions"]

    current = game_state["current"]

    skill = game_state["skill"]

    difficulty = game_state["difficulty"]


    # =================================================
    # GET CURRENT QUESTION
    # =================================================

    q = questions[current]


    # =================================================
    # PATTERN QUESTIONS
    # =================================================

    if skill == "Pattern Recognition":

        question = q["question"]

        sequence = q["sequence"]

        options = q["options"]

        correct_answer = q["answer"]

        target_time = q["time"]


    # =================================================
    # OTHER QUESTIONS
    # =================================================

    else:

        question = q[0]

        correct_answer = q[1]

        target_time = q[2]

        sequence = None

        options = None


    # =================================================
    # SUBMIT ANSWER
    # =================================================

    if request.method == "POST":

        answer = request.form.get(
            "answer",
            ""
        ).strip()


        elapsed = (
            time.time()
            -
            game_state["start_time"]
        )


        # Convert both answers to strings
        # This prevents the Memory integer error.

        correct = (

            str(answer).strip().lower()

            ==

            str(correct_answer).strip().lower()

        )


        performance = calculate_performance(

            correct,

            elapsed,

            target_time

        )


        points = calculate_points(

            performance,

            difficulty

        )


        if correct:

            game_state["correct"] += 1


        game_state["total_performance"] += performance

        game_state["total_points"] += points


        # =================================================
        # SAVE FEEDBACK
        # =================================================

        feedback = {

            "correct": correct,

            "correct_answer": correct_answer,

            "time": round(elapsed, 1),

            "performance": performance,

            "points": points

        }


        # Move to next question

        game_state["current"] += 1


        # =================================================
        # CHECK IF GAME FINISHED
        # =================================================

        finished = (

            game_state["current"]

            >=

            len(questions)

        )


        # =================================================
        # SHOW FEEDBACK
        # =================================================

        return render_template(

            "feedback.html",

            feedback=feedback,

            skill=skill,

            question_number=current + 1,

            total_questions=len(questions),

            finished=finished

        )


    # =================================================
    # START TIMER
    # =================================================

    game_state["start_time"] = time.time()


    # =================================================
    # SHOW QUESTION
    # =================================================

    return render_template(

        "game.html",

        skill=skill,

        difficulty=difficulty.capitalize(),

        question=question,

        sequence=sequence,

        options=options,

        question_number=current + 1,

        total_questions=len(questions)

    )


# =====================================================
# RESULT
# =====================================================

@app.route("/result")
def result():

    if "questions" not in game_state:

        return redirect(
            url_for("home")
        )


    player = load_player()


    total_questions = len(
        game_state["questions"]
    )


    correct_count = game_state["correct"]


    average_performance = round(

        game_state["total_performance"]

        /

        total_questions

    )


    points = game_state["total_points"]


    skill = game_state["skill"]


    # =================================================
    # UPDATE SKILL
    # =================================================

    player["skills"][skill] = average_performance


    # =================================================
    # UPDATE POINTS
    # =================================================

    player["total_points"] += points


    # =================================================
    # UPDATE GAMES
    # =================================================

    player["games_played"] += 1


    # =================================================
    # STREAK
    # =================================================

    if correct_count == total_questions:

        player["streak"] += 1

    else:

        player["streak"] = 0


    if player["streak"] > player["best_streak"]:

        player["best_streak"] = player["streak"]


    # =================================================
    # BADGES
    # =================================================

    badges = player["badges"]


    if player["games_played"] >= 1:

        if "First Challenge" not in badges:

            badges.append(
                "First Challenge"
            )


    if correct_count == total_questions:

        if "Perfect Round" not in badges:

            badges.append(
                "Perfect Round"
            )


    if player["streak"] >= 3:

        if "3 Challenge Streak" not in badges:

            badges.append(
                "3 Challenge Streak"
            )


    if player["total_points"] >= 100:

        if "100 Points" not in badges:

            badges.append(
                "100 Points"
            )


    if average_performance >= 90:

        if "Sharp Mind" not in badges:

            badges.append(
                "Sharp Mind"
            )


    # =================================================
    # SAVE PLAYER
    # =================================================

    save_player(player)


    result_data = {

        "skill": skill,

        "difficulty": game_state["difficulty"],

        "correct": correct_count,

        "total": total_questions,

        "performance": average_performance,

        "points": points

    }


    game_state.clear()


    return render_template(

        "result.html",

        result=result_data,

        player=player

    )


# =====================================================
# RUN
# =====================================================

if __name__ == "__main__":

    app.run(debug=True)


