import json
from pathlib import Path
from app.core.config import settings


class JsonStorage:
    """
    Handles reading and writing Todo data to a JSON file.
    """

    def __init__(self, file_path: str = None):
        self.file_path = Path(file_path) if file_path else Path(settings.DATA_FILE)

    
    def load(self):
        """
        Load todos from the JSON file.
        """
        
        if not self.file_path.exists():
            self.save([])
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                return json.load(file)

        except json.JSONDecodeError:
            return []
        
    def save(self, todos):
        """
        Save todos to the JSON file.
        """

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                todos,
                file, 
                indent=4,
                ensure_ascii=False,
            )


json_storage = JsonStorage()