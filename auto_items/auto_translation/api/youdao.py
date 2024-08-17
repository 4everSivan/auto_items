from . import TranslateApi

API = {
    'youdao': 'http://fanyi.youdao.com/translate',
}


class YouDao(TranslateApi):

    def __init__(self, vip: bool, name: str) -> None:
        super().__init__(vip, name)

    def check(self) -> dict:
        print('run check: ' + type(self).__name__)
        print('is vip: ', self.vip)
        return {}

    @property
    def status(self) -> dict:
        return {}