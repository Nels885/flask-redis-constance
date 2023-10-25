import importlib
from redis import Redis

try:
    settings = importlib.import_module('settings')
except Exception as error:
    print(f"{type(error).__name__}: {error}")
    settings = None


CONFIG = getattr(settings, 'CONSTANCE_CONFIG', {})
CONFIG_FIELDSETS = getattr(settings, 'CONSTANCE_CONFIG_FIELDSETS', {})

REDIS = getattr(settings, 'REDIS', Redis(encoding="utf-8", decode_responses=True))
