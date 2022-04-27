"""
多目的変数最適化　メイン関数
"""
import os
import glob
import argparse
from eval import Evaluator
from download import Downloader
from load import ExcelLoader
from optim import multioptim


def main(args):
    # zipファイルが存在しないならダウンロード
    if not glob.glob("*.zip"):
        Downloader(args.url)()

    if args.mode == "sample":
        # サンプルデータを用いて評価を実行
        Evaluator(args.sample_path, args.exe_path)()

    elif args.mode == "real":
        # Excelファイルを読み取る
        element, constraint = ExcelLoader(args.excel_path)()

        # 多目的最適化を行う
        multioptim(element, constraint)

        # もしevalディレクトリが無ければ作成
        os.makedirs("./eval", exist_ok=True)

        # 評価を実行
        Evaluator(args.input_path, args.exe_path)()

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
    parser.add_argument(
        "--input_path",
        type=str,
        default="./eval",
        help="評価用入力ファイル(pop_vars_eval.txt)のパス名",
    )
    args = parser.parse_args()
    parser.add_argument(
        "--exe_path",
        type=str,
        default="./Mazda_CdMOBP/Mazda_CdMOBP/bin/win64/mazda_mop.exe",
        help="評価時の実行ファイル(mazda_mop.exe)パス名",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["sample", "real"],
        default="real",
        help="モード(sample:サンプルを用いた評価 もしくは real:本番)",
    )
    parser.add_argument(
        "--excel_path",
        type=str,
        default="./Mazda_CdMOBP/Info_Mazda_CdMOBP.xlsx",
        help="データが包含されたExcelファイルのパス名",
    )

    args = parser.parse_args()

    main(args)
