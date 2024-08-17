from . import TranslateApi

API = {
    # 领域翻译 API 手册: https://api.fanyi.baidu.com/product/123
    'vip-baidu': "https://fanyi-api.baidu.com/api/trans/vip/fieldtranslate",
    'baidu': 'https://fanyi-api.baidu.com/api/trans',
}


class Baidu(TranslateApi):

    def __init__(self, vip: bool, name: str) -> None:
        super().__init__(vip, name)

    def check(self) -> dict:
        print('run check: ' + type(self).__name__)
        print('is vip: ', self.vip)
        return {}

    @property
    def status(self) -> dict:
        return {}

    @property
    def url(self) -> str:
        return  API['vip-baidu'] if self.vip else API['baidu']