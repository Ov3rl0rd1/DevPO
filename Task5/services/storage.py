import json
from pathlib import Path

from models.equipment import Equipment


class StorageError(Exception):
    pass


class JsonStorage:
    def __init__(self, path):
        self._path = Path(path)

    def load(self):
        if not self._path.exists():
            return []
        try:
            with self._path.open(encoding="utf-8") as file:
                return [Equipment.from_dict(item) for item in json.load(file)]
        except (OSError, ValueError, TypeError, AttributeError) as error:
            raise StorageError(f"Не удалось прочитать файл {self._path}: {error}") from error

    def save(self, items):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self._path.with_suffix(".tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            json.dump([item.to_dict() for item in items], file, ensure_ascii=False, indent=2)
        temporary_path.replace(self._path)
