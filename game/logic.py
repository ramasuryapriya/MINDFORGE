import time
from game.scoring import calculate_performance, calculate_points


QUESTIONS = {

    "easy": [
        ("2, 6, 12, 20, 30, ?", "42", 20),
        ("1, 4, 9, 16, 25, ?", "36", 20),
        ("5, 10, 15, 20, ?", "25", 15)
    ],

    "medium": [
        ("3, 8, 15, 24, 35, ?", "48", 20),
        ("4, 9, 16, 25, 36, ?", "49", 20),
        ("2, 5, 10, 17, 26, ?", "37", 20)
    ],

    "hard": [
        ("5, 11, 19, 29, 41, ?", "55", 25),
        ("2, 6, 12, 20, 30, 42, ?", "56", 25),
        ("3, 7, 13, 21, 31, ?", "43", 25)
    ]
}


def logic_challenge(difficulty):

    questions = QUESTIONS[difficulty]

    correct_count = 0
    total_performance = 0
    total_points = 0

    print("\n🧠 LOGIC ROUND")
    print("Difficulty:", difficulty.capitalize())
    print("Questions:", len(questions))

    for index, (question, correct_answer, target_time) in enumerate(questions, 1):

        print(f"\nQuestion {index}/{len(questions)}")
        print(question)

        start = time.time()

        answer = input("Your answer: ")

        elapsed = time.time() - start

        correct = answer.strip() == correct_answer

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

    average_performance = round(
        total_performance / len(questions)
    )

    return (
        correct_count == len(questions),
        average_performance,
        total_points
    )