import os

from auto_translation.exception import ProcessingFileException


def check_file(file_path: str) -> bool:

    if not isinstance(file_path, str):
        error_msg = '{} is not a path'.format(file_path)
        raise ProcessingFileException(error_msg)

    if not os.path.exists(file_path):
        error_msg = '{} is not exists'.format(file_path)
        raise ProcessingFileException(error_msg)

    if not os.path.isfile(file_path):
        error_msg = "{} is not a file".format(file_path)
        raise ProcessingFileException(error_msg)

    if not os.access(file_path, os.R_OK) or not os.access(file_path, os.W_OK):
        error_msg = 'permission denial : {}'.format(file_path)
        raise ProcessingFileException(error_msg)

    if os.stat(file_path).st_size == 0:
        error_msg = '{} is an empty file'.format(file_path)
        raise ProcessingFileException(error_msg)

    return True


def make_save_file(save_path: str, file_name: str) -> dict:
    if not isinstance(save_path, str):
        error_msg = '{} is not a path'.format(save_path)
        raise ProcessingFileException(error_msg)

    if os.path.exists(save_path):
        if not os.path.isdir(save_path):
            error_msg = "{} is not a dir ".format(save_path)
            raise ProcessingFileException(error_msg)

        if not os.access(save_path, os.R_OK) or not os.access(save_path, os.W_OK):
            error_msg = 'permission denial : {}'.format(save_path)
            raise ProcessingFileException(error_msg)

        if os.stat(save_path).st_size == 0:
            error_msg = '{} is an empty file'.format(save_path)
            raise ProcessingFileException(error_msg)

        try:
            file_name, file_type = file_name.split('.', 1)
            save_file_path = save_path.rsplit('/', 1)[0] + '/' + file_name + '_trans' + '.{0}'.format(file_type)
            with open(save_file_path, "w"):
                pass
            return {'state': True, 'path': save_file_path}
        except Exception as e:
            raise Exception(e)
    else:
        try:
            os.makedirs(save_path)

            if not os.access(save_path, os.R_OK) or not os.access(save_path, os.W_OK):
                error_msg = 'permission denial : {}'.format(save_path)
                raise ProcessingFileException(error_msg)

            save_file_path = save_path.rsplit('/', 1)[0] + '/' + file_name
            with open(save_file_path, "w"):
                pass
            return {'state': True, 'path': save_file_path}
        except Exception as e:
            raise Exception(e)


def save_data(file_path: str, data_lst: list) -> None:
    with open(file_path, 'w+', encoding='utf-8') as file:
        for line in data_lst:
            file.write(line)
