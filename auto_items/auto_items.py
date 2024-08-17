import argparse
import sys

from .auto_translation.__main__ import translation, API
from .banner import BANNER


def main() -> None:
    parser = argparse.ArgumentParser(description="AUTO_ITEMS 自动化工具集")
    # 翻译
    subparsers = parser.add_subparsers(title='Command', dest='Command', help='已实现的功能')
    sub_trans = subparsers.add_parser('translate', help='文档翻译功能')
    sub_trans.add_argument('-i', '--input', type=str, help='输入文件路径', required=True)
    sub_trans.add_argument('-o', '--output', type=str, help='输出文件路径', default='.', required=False)
    sub_trans.add_argument('-l', '--language', type=str, help='翻译语言', default='English', required=False)
    sub_trans.add_argument('-a', '--api', type=str, help='选择翻译API', choices= API,
                           default='youdao', required=False)
    sub_trans.add_argument('-c', '--check', type=bool, help='检查API连通性', required=False)
    order = subparsers.add_parser('grab', help='订票功能')

    args = parser.parse_args()
    if args.Command is None:
        print(BANNER)
        parser.print_help()
        sys.exit(1)

    if args.Command == 'translate':
        translation(vars(args))
