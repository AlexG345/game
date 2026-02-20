from pathlib import Path

class Config:

	def __init__(self):
		self.SRC_DIR = Path(__file__).resolve().parent.parent
		self.PROJECT_DIR = self.SRC_DIR.parent
		self.ASSETS_DIR = self.PROJECT_DIR / "assets"

	def get_asset_path(self, filename):
		return self.ASSETS_DIR / filename


def is_path(value):
	return isinstance(value, (str, Path))

CONFIG = Config()