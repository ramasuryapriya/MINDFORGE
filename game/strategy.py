import time
from game.scoring import calculate_performance, calculate_points



QUESTIONS = {

    "easy": [

        (
            "You have 3 tasks: A takes 10 minutes, B takes 5 minutes, "
            "and C takes 15 minutes. Which task should you do first "
            "if you want to finish the shortest task first? "
            "Answer A, B or C.",
            "B",
            20
        ),

        (
            "You have ₹100. You buy a book for ₹60. "
            "How much money is left?",
            "40",
            15
        ),

        (
            "You have two routes. Route A takes 20 minutes. "
            "Route B takes 10 minutes. Which route is faster? "
            "Answer A or B.",
            "B",
            15
        )

    ],


    "medium": [

        (
            "You have 3 tasks: A=20 minutes, B=10 minutes, C=30 minutes. "
            "If you want to finish the shortest task first, "
            "which task should you choose? Answer A, B or C.",
            "B",
            20
        ),

        (
            "You have ₹500. You spend ₹200 and then ₹100. "
            "How much money remains?",
            "200",
            20
        ),

        (
            "A project has 4 tasks. A takes 5 minutes, B takes 15 minutes, "
            "C takes 10 minutes and D takes 20 minutes. "
            "If you want to finish the shortest task first, "
            "which task should you choose?",
            "A",
            20
        )

    ],


    "hard": [

        (
            "You have 4 tasks: A=20 minutes, B=5 minutes, "
            "C=10 minutes and D=15 minutes. "
            "If you must complete the two shortest tasks first, "
            "which two tasks should you choose? Answer like B,C.",
            "B,C",
            25
        ),

        (
            "You have ₹1000. You spend ₹250 on food and ₹150 on travel. "
            "How much money remains?",
            "600",
            20
        ),

        (
            "Three routes take 30, 20 and 15 minutes. "
            "You need to reach your destination as quickly as possible. "
            "Which route should you choose? Answer 15.",
            "15",
            20
        )

    ]

}




def strategy_challenge(difficulty):

    questions = QUESTIONS[difficulty]

    correct_count = 0
    total_performance = 0
    total_points = 0

    print("\n🎯 STRATEGY ROUND")
    print("Difficulty:", difficulty.capitalize())

    for index, (question, correct_answer, target_time) in enumerate(questions, 1):

        print(f"\nQuestion {index}/{len(questions)}")
        print(question)

        start = time.time()

        answer = input("Your choice: ")

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
            print("✅ Good strategic decision!")
            correct_count += 1
        else:
            print("❌ Not the best choice.")
            print("Correct choice:", correct_answer)

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