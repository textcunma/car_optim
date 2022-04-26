"""
多目的変数最適化
"""

import glob
import argparse
from download import Downloader


def main(args):
    if not glob.glob("*.zip"):  # zipファイルが存在しないなら
        Downloader(args.url)()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="メインスクリプト")
    parser.add_argument(
        "--url",
        type=str,
        default="https://ladse.eng.isas.jaxa.jp/benchmark/Mazda_CdMOBP.zip",
        help="データのURL",
    )
    args = parser.parse_args()

    main(args)
