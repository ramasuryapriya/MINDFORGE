def calculate_performance(correct, time_taken, target_time):
    if not correct:
        accuracy = 0
    else:
        accuracy = 100

    if time_taken <= target_time:
        time_score = 100
    else:
        extra_time = time_taken - target_time
        time_score = max(0, 100 - (extra_time * 5))

    performance = (accuracy * 0.7) + (time_score * 0.3)

    return round(performance)


def calculate_points(performance, difficulty):
    if performance < 40:
        return 5

    base_points = {
        "easy": 10,
        "medium": 20,
        "hard": 30
    }

    points = base_points.get(difficulty, 10)

    return round(points * (performance / 100))