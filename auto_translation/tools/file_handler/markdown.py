from . import AbstractFileHandler


class Markdown(AbstractFileHandler):

    def __init__(self, file_path: str) -> None:
        super(Markdown, self).__init__(file_path)

    def get_lines_lst(self) -> list:
        res = []
        with open(self.file_path, "r+", encoding='utf-8') as file:
            for line in file:
                if line != '\n':
                    res.append(line)

        return res

    @staticmethod
    def cut_line(line: str) -> dict:
        res = []
        if line in ['', ' ', '\n']:
            return {'state': False, 'line': line}
        elif "`" in line:
            return {'state': False, 'line': line}
        elif "#" in line:
            if line[0] == '#':
                res.append('#')
                for i in line.rsplit("#", 1):
                    res.append(i)
            return {'state': True, 'line': res}
        elif ">" in line:
            res = line.rsplit(">", 1)
            return {'state': True, 'line': res}
        elif "*" in line:
            res = line.split('*')
            return {'state': True, 'line': res}
