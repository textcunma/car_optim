"""
多目的変数最適化
"""

import glob
import argparse
from download import Downloader
from eval import Evaluator

def main(args):
    if not glob.glob("*.zip"):  # zipファイルが存在しないなら
        Downloader(args.url)()

    if args.mode == "sample":
        Evaluator(args.sample_path, args.exe_path)()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="メインスクリプト")
    parser.add_argument(
        "--url",
        type=str,
        default="https://ladse.eng.isas.jaxa.jp/benchmark/Mazda_CdMOBP.zip",
        help="データのURL",
    )
    parser.add_argument(
        "--sample_path",
        type=str,
        default="./Mazda_CdMOBP/Mazda_CdMOBP/sample",
        help="サンプル入力ファイル(pop_vars_eval.txt)のパス名",
    )
    args = parser.parse_args()
    parser.add_argument(
        "--exe_path",
        type=str,
        default="./Mazda_CdMOBP/Mazda_CdMOBP/bin/win64/mazda_mop.exe",
        help="評価時の実行ファイル(mazda_mop.exe)パス名"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["sample", "eval"],
        default="sample",
        help="評価モード(sample:サンプルを用いた評価 もしくは eval:本番評価)",
    )
    args = parser.parse_args()

    main(args)
