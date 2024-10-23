import importlib
from redis import Redis

try:
    user_settings = importlib.import_module('settings')
except Exception as error:
    print(f"{type(error).__name__}: {error}")
    user_settings = None


CONFIG = getattr(user_settings, 'CONSTANCE_CONFIG', {})
CONFIG_FIELDSETS = getattr(user_settings, 'CONSTANCE_CONFIG_FIELDSETS', {})

REDIS = getattr(user_settings, 'REDIS', Redis(encoding="utf-8", decode_responses=True))
