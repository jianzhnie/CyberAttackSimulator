import os
import sys

sys.path.append(os.getcwd())
from cyberattacksim.game_modes.game_mode_db import GameModeDB

if __name__ == '__main__':
    db = GameModeDB()
    db.rebuild_db()
