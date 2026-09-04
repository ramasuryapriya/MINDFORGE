class MindProfile:

    def __init__(self, skills=None, total_points=0,
                 games_played=0, streak=0, best_streak=0,
                 badges=None):

        self.skills = skills or {
            "Logic": 0,
            "Pattern Recognition": 0,
            "Memory": 0,
            "Strategy": 0,
            "Attention": 0
        }

        self.total_points = total_points
        self.games_played = games_played
        self.streak = streak
        self.best_streak = best_streak
        self.badges = badges or []

    def update_skill(self, skill, performance):

        old_score = self.skills[skill]

        # First assessment
        if old_score == 0:
            new_score = performance
        else:
            # 70% previous ability + 30% new performance
            new_score = (old_score * 0.7) + (performance * 0.3)

        self.skills[skill] = round(max(0, min(100, new_score)))

    def add_points(self, points):
        self.total_points += points

    def update_streak(self, correct):

        if correct:
            self.streak += 1

            if self.streak > self.best_streak:
                self.best_streak = self.streak
        else:
            self.streak = 0

    def get_level(self):
        return (self.total_points // 100) + 1

    def check_badges(self):

        if self.games_played >= 1:
            self.add_badge("First Thought")

        if self.streak >= 3:
            self.add_badge("Hot Streak")

        if self.games_played >= 10:
            self.add_badge("Mind Explorer")

        if any(score >= 80 for score in self.skills.values()):
            self.add_badge("Sharp Mind")

        if all(score > 0 for score in self.skills.values()):
            self.add_badge("MindForge Explorer")

    def add_badge(self, badge):

        if badge not in self.badges:
            self.badges.append(badge)

    def display_profile(self):

        print("\n🧠 Your Mind Profile")
        print("--------------------")

        for skill, score in self.skills.items():
            status = "Not assessed" if score == 0 else f"{score}%"
            print(f"{skill}: {status}")

        print("\n⭐ Points:", self.total_points)
        print("🏆 Level:", self.get_level())
        print("🔥 Current Streak:", self.streak)
        print("🔥 Best Streak:", self.best_streak)

        if self.badges:
            print("\n🏅 Badges:")
            for badge in self.badges:
                print("•", badge)