import json
import os


PLAYER_FILE = "data/player.json"


def load_player():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(PLAYER_FILE):

        player = {
            "skills": {
                "Logic": 0,
                "Pattern Recognition": 0,
                "Memory": 0,
                "Strategy": 0,
                "Attention": 0
            },
            "total_points": 0,
            "games_played": 0,
            "streak": 0,
            "best_streak": 0,
            "badges": []
        }

        save_player(player)

        return player

    with open(PLAYER_FILE, "r") as file:
        return json.load(file)


def save_player(player):

    os.makedirs("data", exist_ok=True)

    with open(PLAYER_FILE, "w") as file:
        json.dump(player, file, indent=4)