import sys

import requests
import logging
import os

from exception import TranslationException
from tools.file_handler import get_file_handler, AbstractFileHandler
from tools import check_file, make_save_file, save_data


logger = logging.getLogger()
URL = {
    'youdao': 'http://fanyi.youdao.com/translate',
}


def prepare_to_translation(sv_path, file_name: str) -> dict:
    return make_save_file(sv_path, file_name).get('path')


def get_params(api_tec: str, text: str) -> dict:
    if api_tec not in URL.keys():
        error_msg = "{} is not support".format(api_tec)
        return {'state': False, 'error_msg': error_msg}

    if api_tec == 'youdao':
        params = {
            "type": "Auto",
            "i": text,
            "doctype": "json",
            "version": "2.1"
        }
    else:
        params = {}
    return params


def translate(t_url: str, api_tec: str, f_handler: AbstractFileHandler, data_lst: list) -> list:
    res = []
    for li in data_lst:
        d = f_handler.cut_line(li)
        if not d.get('state'):
            res.append(d)
        else:
            new_line = str()
            for q in d.get('line'):
                if q[0] in ['*', ">", "#", "`"]:
                    new_line.join(q)
                else:
                    param = get_params(api_tec, q)
                    response = requests.post(t_url, params=param)

                    if response.status_code == 200:
                        data = response.json().get('translateResult')[0][0].get('tgt')
                        new_line.join(data)
                    else:
                        error_msg = 'Failed to post data: {}'.format(response.status_code)
                        logger.error(error_msg)
            res.append(new_line)

    return res


if __name__ == '__main__':
    try:
        dir_path = os.path.dirname(__file__)
        file_path = dir_path + '/sample/' + 'test.md'
        save_path = dir_path + '/translation/'
        api_name = 'youdao'
        url = URL.get(api_name)

        # check file
        check_file(file_path)

        # get file handler
        file_handler = get_file_handler(file_path)
        data_list = file_handler.get_lines_lst()

        # prepare to translation
        save_path_file = prepare_to_translation(save_path, file_handler.file_name)
        for line in data_list:
            file_handler.cut_line(line)
            print(line)

        sys.exit()

        new_data_lst = translate(url, api_name, file_handler, data_list)
        print(new_data_lst)
        # save new data
        # save_data(save_path_file, new_data_lst)
    except TranslationException as e:
        logger.exception(e)
    except Exception as e:
        logger.exception(e)
