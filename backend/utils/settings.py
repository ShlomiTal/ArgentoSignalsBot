import json
import os

SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "../settings.json")

def load_settings():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("[Settings Error]", e)
        return {}

def update_setting(key, value):
    settings = load_settings()
    settings[key] = value
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print("[Settings Update Error]", e)
        return False

def get_setting(key, default=None):
    settings = load_settings()
    return settings.get(key, default)
