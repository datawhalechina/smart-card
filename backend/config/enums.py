from enum import Enum



class RedisInitKeyConfig(Enum):
    """
    系统内置Redis键名
    """

    @property
    def key(self):
        return self.value.get('key')

    @property
    def remark(self):
        return self.value.get('remark')

    ACCESS_TOKEN = {'key': 'access_token', 'remark': '登录令牌信息'}
    SYS_DICT = {'key': 'sys_dict', 'remark': '数据字典'}
    SYS_CONFIG = {'key': 'sys_config', 'remark': '配置信息'}
    CAPTCHA_CODES = {'key': 'captcha_codes', 'remark': '图片验证码'}
    ACCOUNT_LOCK = {'key': 'account_lock', 'remark': '用户锁定'}
    PASSWORD_ERROR_COUNT = {'key': 'password_error_count', 'remark': '密码错误次数'}
    SMS_CODE = {'key': 'sms_code', 'remark': '短信验证码'}
