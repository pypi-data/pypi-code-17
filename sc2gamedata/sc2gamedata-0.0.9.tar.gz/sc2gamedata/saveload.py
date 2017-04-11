import pickle
from . import GameData

_cache_path = "ladder_data.cache"


def save_to_cache(ladder_data: GameData):
    with open(_cache_path, mode='wb') as file_at_path:
        pickle.dump(ladder_data, file_at_path)


def load_cache() -> GameData:
    with open(_cache_path, mode='rb') as file_at_path:
        return pickle.load(file_at_path)
