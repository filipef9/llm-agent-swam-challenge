import os

from dotenv import load_dotenv


class Configuration:

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self) -> dict:
        _ = load_dotenv()
        return {
            "APITitle": os.getenv("API_TITLE"),
            "APIVersion": os.getenv("API_VERSION"),
            "APIDescription": os.getenv("API_DESCRIPTION"),
            "APIRootPath": os.getenv("API_ROOT_PATH"),
        }
