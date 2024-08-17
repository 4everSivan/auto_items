import os
import sys
import inspect
import pkgutil
import importlib
import logging

from auto_items.auto_translation.exception import FileHandlerException

logger = logging.getLogger()
FILE_EXTENSION_DICT = {
    'md': 'markdown',
    'txt': 'text'
   }


def handler_modules() -> list:
    dcs_dirname = os.path.dirname(__file__)
    module_prefix = __package__ + '.'

    if getattr(sys, 'frozen', False):
        toc = set()
        for importer in pkgutil.iter_importers():
            if hasattr(importer, 'toc'):
                toc |= importer.toc
        return [module for module in toc if module.startswith(module_prefix) and module.count('.') == 2]
    else:
        return [module_prefix + name for _, name, is_pkg in pkgutil.iter_modules([dcs_dirname]) if not is_pkg]


def get_file_handler(file_path: str) -> 'AbstractFileHandler':
    # get file extension
    file_name = file_path.rsplit('/', 1)[1]
    file_extension = file_name.rsplit('.', 1)[1] if '.' in file_name else 'txt'
    if file_extension not in FILE_EXTENSION_DICT.keys():
        error_msg = 'not support extension: {}'.format(file_extension)
        raise FileHandlerException(error_msg)
    else:
        file_extension = FILE_EXTENSION_DICT.get(file_extension)

    handlers = handler_modules()

    for module_name in handlers:
        name = module_name.split('.')[-1]
        if file_extension == name:
            try:
                module = importlib.import_module(module_name)
                for key, item in module.__dict__.items():
                    if key.lower() == name and inspect.isclass(item) and issubclass(item, AbstractFileHandler):
                        return item(file_path)
            except ImportError:
                raise FileHandlerException('Failed to import {}'.format(module_name))


class AbstractFileHandler(object):

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.file_name = file_path.rsplit('/', 1)[1]

    def get_lines_lst(self) -> list:
        """return line list"""

    @staticmethod
    def cut_line(line: str) -> dict:
        """cut line"""
