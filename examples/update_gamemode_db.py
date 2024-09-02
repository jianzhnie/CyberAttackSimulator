import json
import os
import sys

sys.path.append(os.getcwd())
from cyberattacksim.game_modes.game_mode import (GameMode,
                                                 default_game_mode_path)
from cyberattacksim.game_modes.game_mode_db import GameModeDB

if __name__ == '__main__':
    db = GameModeDB()
    db.rebuild_db()

    gamemode = GameMode().create_from_yaml(default_game_mode_path())
    game_dict = gamemode.to_dict()

    # 将字典保存为 JSON 文件
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(game_dict, json_file, ensure_ascii=False, indent=4)
