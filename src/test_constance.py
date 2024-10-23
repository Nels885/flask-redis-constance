from constance import config, redis_get, redis_set, redis_mset, REDIS


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


app = WebApp()


class TestConstance:

    @classmethod
    def setup_class(cls):
        config.init_app(app)
        config.reset_all()

    @classmethod
    def teardown_class(cls):
        for key in app.config.get('CONSTANCE_CONFIG', {}).keys():
            REDIS.delete(key)

    def test_config_init_app(self):
        fields = config.get_fields('GROUP1')
        assert fields == {'KEY1': ('value1', 'value1', 'description1'), 'KEY2': (0, 0, 'description2')}

    def test_config_get_value(self):
        assert config.KEY1 == 'value1'
        assert config.KEY2 == 0

    def test_config_set_value(self):
        for value in ['value1', 'value2', 250000]:
            config.KEY1 = value
            assert config.KEY1 == value
            assert config.KEY1 == redis_get('KEY1')

    def test_redis_get(self):
        assert redis_get('test', 'test') == 'test'

    def test_redis_set(self):
        for value in ['value1', 'value2', 250000]:
            assert redis_set('KEY1', value) is True
            assert redis_get('KEY1') == value

    def test_redis_mset(self):
        for value in ['value1', 'value2', 250000]:
            assert redis_mset({'KEY2': value}) is True
            assert redis_mset(KEY2=value) is True
            assert redis_get('KEY2') == value
