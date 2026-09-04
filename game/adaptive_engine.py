class AdaptiveEngine:

    def choose_skill(self, skills):

        # Play unassessed skills first
        unassessed = [
            skill for skill, score in skills.items()
            if score == 0
        ]

        if unassessed:
            return unassessed[0]

        # Otherwise choose weakest skill
        return min(skills, key=skills.get)

    def choose_difficulty(self, skill_score):

        if skill_score == 0:
            return "easy"

        if skill_score < 50:
            return "easy"

        elif skill_score < 75:
            return "medium"

        else:
            return "hard"