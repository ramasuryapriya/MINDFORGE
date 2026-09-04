import time
from game.scoring import calculate_performance, calculate_points



QUESTIONS = {

    "easy": [

        (
            "How many times does 7 appear? "
            "3 7 2 7 9 1 7 5",
            "3",
            15
        ),

        (
            "Which number appears only once? "
            "4 6 4 8 6 4",
            "8",
            15
        ),

        (
            "Find the different number: "
            "5 5 5 5 8 5 5",
            "8",
            15
        )

    ],


    "medium": [

        (
            "How many times does 3 appear? "
            "3 8 3 5 9 3 1 3 6",
            "4",
            20
        ),

        (
            "Which number appears only once? "
            "2 7 5 2 9 7 2",
            "5",
            20
        ),

        (
            "Find the different number: "
            "6 6 6 9 6 6 6 6",
            "9",
            20
        )

    ],


    "hard": [

        (
            "How many times does 4 appear? "
            "4 8 2 4 7 9 4 1 6 4 3 4",
            "5",
            25
        ),

        (
            "Which number appears only once? "
            "8 3 5 8 3 5 8 2 3",
            "2",
            25
        ),

        (
            "Find the different number: "
            "7 7 7 7 7 1 7 7 7",
            "1",
            25
        )

    ]

}




def attention_challenge(difficulty):

    questions = QUESTIONS[difficulty]

    correct_count = 0
    total_performance = 0
    total_points = 0

    print("\n👀 ATTENTION ROUND")
    print("Difficulty:", difficulty.capitalize())

    for index, (sequence, correct_answer, target_time) in enumerate(questions, 1):

        print(f"\nQuestion {index}/{len(questions)}")

        print(sequence)

        print("Find the FIRST position containing 7.")

        start = time.time()

        answer = input("Position: ")

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
            print("✅ Excellent attention!")
            correct_count += 1
        else:
            print("❌ Incorrect.")
            print("Correct position:", correct_answer)

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