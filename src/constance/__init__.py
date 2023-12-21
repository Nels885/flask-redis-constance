from wtforms import Form, IntegerField, BooleanField, StringField

from . import settings
from .settings import REDIS


FIELDS = {
    str: (StringField, {}),
    bool: (BooleanField, {'required': False}),
    int: (IntegerField, {}),
}


def redis_mset(*args, **kwargs):
    if args and isinstance(args[0], dict):
        REDIS.mset(args[0])
    if kwargs:
        REDIS.mset(kwargs)


def redis_get(key, default=''):
    value = REDIS.get(key)
    if not value:
        return default
    return value


class ConstanceForm(Form):

    def __init__(self, initial, *args, **kwargs):
        super().__init__(*args, initial=initial, **kwargs)

        for name, options in settings.CONFIG:
            default = options[0]
            if len(options) == 3:
                pass
            else:
                config_type = type(default)

            field_class, kwargs = FIELDS[config_type]
            self.fields[name] = field_class(label=name, **kwargs)


class Config:

    def __init__(self, *args, **kwargs):
        self.config = settings.CONFIG
        self.fieldsets = settings.CONFIG_FIELDSETS
        self._addattribute()

    def __setattr__(self, __name: str, __value) -> None:
        if isinstance(__value, str):
            REDIS.set(__name, __value)
        self.__dict__[__name] = __value

    def __getattribute__(self, __name: str) -> str:
        """
        Retrieving attribute value
        """
        try:
            if isinstance(__name, str) and __name.upper() in REDIS.keys():
                value = REDIS.get(__name.upper())
                if value.isnumeric():
                    return int(value)
                return value
            return super().__getattribute__(__name)
        except AttributeError:
            raise KeyError(f" value {__name} does not exist in constance")

    def _addattribute(self) -> None:
        if self.config and isinstance(self.config, dict):
            for key, value in self.config.items():
                if isinstance(key, str) and isinstance(value, tuple) and len(value) == 2:
                    key = key.upper()
                    if key not in REDIS.keys():
                        REDIS.set(key, value[0])
                    setattr(self, key, REDIS.get(key))

    def init_app(self, app):
        self.config = app.config.get('CONSTANCE_CONFIG', {})
        self.fieldsets = app.config.get('CONSTANCE_CONFIG_FIELDSETS', {})
        self._addattribute()

    def set(self, key, value):
        self.__setattr__(key, value)
        return value

    def get_fields(self, name="all") -> dict:
        if name == "all":
            fields = list(self.config)
        fields = self.fieldsets.get(name, '')
        return {key: (self.config.get(key)[0], REDIS.get(key), self.config.get(key)[1]) for key in fields}

    def get_default(self, key: str) -> str:
        value = self.__dict__.get(key, '')
        if isinstance(value, tuple) and len(value) == 2:
            return value[0]
        return ""

    def set_fields(self, fields: dict) -> dict:
        for key, value in fields.items():
            setattr(self, key, value)

    def reset(self, key: str):
        value = settings.CONFIG.get(key, '')
        if value:
            REDIS.set(key, value[0])
            setattr(self, key, REDIS.get(key))
            return self.__dict__[key]
        return None


config = Config()
