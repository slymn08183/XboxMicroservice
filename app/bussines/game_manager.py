from app.bussines.xbox_mini_main import get_all_game_data_xbox


class GameManager:
    def __init__(self, is_update):
        get_all_game_data_xbox('tr', 'TR', is_update)
