import time
from game.scoring import calculate_performance, calculate_points

QUESTIONS = {

    "easy": [

        {
            "question": "Which direction comes next?",
            "sequence": ["↑", "→", "↓"],
            "options": ["↑", "→", "↓", "←"],
            "answer": "←",
            "time": 15
        },

        {
            "question": "Which pattern comes next?",
            "sequence": ["●", "●●", "●●●"],
            "options": ["●", "●●", "●●●●", "▲▲"],
            "answer": "●●●●",
            "time": 15
        },

        {
            "question": "Which shape comes next?",
            "sequence": ["▲", "●", "▲", "●"],
            "options": ["▲", "●", "■", "◆"],
            "answer": "▲",
            "time": 15
        }

    ],


    "medium": [

        {
            "question": "The dot moves right each step. What comes next?",
            "sequence": [
                "● □ □",
                "□ ● □",
                "□ □ ●"
            ],
            "options": [
                "● □ □",
                "□ ● □",
                "□ □ ●",
                "● ● □"
            ],
            "answer": "● □ □",
            "time": 20
        },

        {
            "question": "The arrow rotates clockwise. What comes next?",
            "sequence": ["↑", "→", "↓"],
            "options": ["↑", "→", "↓", "←"],
            "answer": "←",
            "time": 20
        },

        {
            "question": "One square is added each step. What comes next?",
            "sequence": ["■", "■■", "■■■", "■■■■"],
            "options": [
                "■■",
                "■■■■",
                "■■■■■",
                "■■■■■■"
            ],
            "answer": "■■■■■",
            "time": 20
        }

    ],


    "hard": [

        {
            "question": "Complete the visual pattern.",
            "sequence": [
                "●",
                "●●",
                "●●●"
            ],
            "options": [
                "●",
                "●●",
                "●●●●",
                "●●●●●"
            ],
            "answer": "●●●●",
            "time": 25
        },

        {
            "question": "The triangle moves to the next position. What comes next?",
            "sequence": [
                "▲ □ □ □",
                "□ ▲ □ □",
                "□ □ ▲ □",
                "□ □ □ ▲"
            ],
            "options": [
                "▲ □ □ □",
                "□ ▲ □ □",
                "□ □ ▲ □",
                "□ □ □ ▲"
            ],
            "answer": "▲ □ □ □",
            "time": 25
        },

        {
            "question": "The shapes repeat in order. What comes next?",
            "sequence": ["○", "△", "□", "○"],
            "options": [
                "○",
                "△",
                "□",
                "◇"
            ],
            "answer": "△",
            "time": 25
        }

    ]

}



def pattern_challenge(difficulty):

    questions = QUESTIONS[difficulty]

    correct_count = 0
    total_performance = 0
    total_points = 0

    print("\n🔍 PATTERN RECOGNITION ROUND")
    print("Difficulty:", difficulty.capitalize())

    for index, (question, correct_answer, target_time) in enumerate(questions, 1):

        print(f"\nQuestion {index}/{len(questions)}")
        print(question)

        if correct_answer in ["1", "2", "3", "4"]:
            print("1. ●")
            print("2. ○")
            print("3. ▲")
            print("4. ■")

        start = time.time()

        answer = input("Your answer: ")

        elapsed = time.time() - start

        correct = answer.strip().upper() == correct_answer

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
            print("✅ Correct!")
            correct_count += 1
        else:
            print("❌ Incorrect.")
            print("Correct answer:", correct_answer)

        print(f"⏱️ Time: {elapsed:.1f}s")
        print(f"📊 Performance: {performance}%")
        print(f"⭐ Points: +{points}")

        total_performance += performance
        total_points += points

    return (
        correct_count == len(questions),
        round(total_performance / len(questions)),
        total_points
    )