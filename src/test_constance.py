from constance import config, redis_get


class WebApp():

    def __init__(self):
        self.config = {
            'CONSTANCE_CONFIG': {
                'KEY1': ('value1', 'description1'),
                'KEY2': (0, 'description2'),
            },
            'CONSTANCE_CONFIG_FIELDSETS': {
                'GROUP1': ('KEY1', 'KEY2')
            }
        }


def test_config_init_app():
    app = WebApp()
    config.init_app(app)
    fields = config.get_fields('GROUP1')
    assert fields == {'KEY1': ('value1', 'value1', 'description1'), 'KEY2': (0, 0, 'description2')}


def test_config_get_value():
    assert config.KEY1 == 'value1'
    assert config.KEY2 == 0


def test_redis_get():
    assert redis_get('test', 'test') == 'test'
