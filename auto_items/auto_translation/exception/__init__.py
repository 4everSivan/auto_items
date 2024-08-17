class TranslationException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        """
        >>> str(TranslationException('foo'))
        "'foo'"
        """
        return repr(self.value)


class NoneInputException(TranslationException):
    """None input exception"""


class FileHandlerException(TranslationException):
    """file handler exception"""


class ProcessingFileException(TranslationException):
    """check file exception"""
