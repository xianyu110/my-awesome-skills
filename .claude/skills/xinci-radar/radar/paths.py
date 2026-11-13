from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
CACHE = ROOT / "cache"
DB_PATH = DATA / "radar.db"
PUBLISHED_STATE = DATA / "published_state.json"
SITES_YAML = CONFIG / "sites.yaml"
ROOTS_JSON = CONFIG / "roots.json"
SYNONYMS_JSON = CONFIG / "synonyms.json"
