import os
import sys
import pkgutil
import importlib
import inspect

from typing import Set, List

API = ['baidu', 'vip-baidu', 'youdao']


def api_modules() -> List[str]:
    api_dirname = os.path.dirname(__file__)
    module_prefix = __package__ + '.'

    if getattr(sys, 'frozen', False):
        toc: Set[str] = set()
        # dcs_dirname may contain a dot, which causes pkgutil.iter_importers()
        # to misinterpret the path as a package name. This can be avoided
        # altogether by not passing a path at all, because PyInstaller's
        # FrozenImporter is a singleton and registered as top-level finder.
        for importer in pkgutil.iter_importers():
            if hasattr(importer, 'toc'):
                toc |= getattr(importer, 'toc')
        return [module for module in toc if module.startswith(module_prefix) and module.count('.') == 2]

    return [module_prefix + name for _, name, is_pkg in pkgutil.iter_modules([api_dirname]) if not is_pkg]


def find_api_class(module: type(sys)) -> type:
    module_name = module.__name__.rpartition('.')[2]
    return next(
        (obj for obj_name, obj in module.__dict__.items()
         if (obj_name.lower() == module_name
             and inspect.isclass(obj) and issubclass(obj, TranslateApi))),
        None)

def get_api(name: str) -> 'TranslateApi':
    for api in api_modules():
        is_vip, name = (True, name.split('-',1)[1]) if "-" in name else (False, name)
        if name in api:
            try:
                api_module = importlib.import_module(api)
                api_class = find_api_class(api_module)
                return api_class(is_vip, name)
            except ImportError as e:
                print(e)


class TranslateApi:
    def __init__(self, vip: bool, name: str) -> None:
        self.vip = vip
        self.name = name
        self.lang = 'English'

    def check(self) -> dict:
        """return check result"""


    def status(self) -> dict:
        """return api state"""

    def url(self) -> str:
        """return api url"""

    def set_language(self, lang: str) -> None:
        self.lang = lang
