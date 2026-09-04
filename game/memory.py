import time
from game.scoring import calculate_performance, calculate_points



QUESTIONS = {

    "easy": [
        ("7 2 9 4", "7294", 15),
        ("3 8 1 6", "3816", 15),
        ("5 1 7 2", "5172", 15)
    ],

    "medium": [
        ("8 3 6 1 9 4", "836194", 20),
        ("2 7 4 9 1 6", "274916", 20),
        ("5 8 2 6 3 7", "582637", 20)
    ],

    "hard": [
        ("9 4 7 2 8 1 5 3", "94728153", 25),
        ("6 2 9 4 1 8 5 7", "62941857", 25),
        ("3 8 5 1 7 4 9 2", "38517492", 25)
    ]

}




def memory_challenge(difficulty):

    questions = QUESTIONS[difficulty]

    correct_count = 0
    total_performance = 0
    total_points = 0

    print("\n🧠 MEMORY ROUND")
    print("Difficulty:", difficulty.capitalize())

    for index, (sequence, length, target_time) in enumerate(questions, 1):

        print(f"\nQuestion {index}/{len(questions)}")
        print("Memorize:")

        print(sequence)

        time.sleep(2 if difficulty == "easy" else 3)

        print("\n" * 20)

        start = time.time()

        answer = input("Enter the sequence: ")

        elapsed = time.time() - start

        correct = (
            answer.replace(" ", "")
            == sequence.replace(" ", "")
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
            print("✅ Correct!")
            correct_count += 1
        else:
            print("❌ Incorrect.")
            print("Correct sequence:", sequence)

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