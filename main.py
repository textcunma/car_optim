import os
import glob
import argparse
from eval import Evaluator
from load import ExcelLoader
from optim import MultiOptim
from download import Downloader


def main(args):
    # zipファイルが存在しないならダウンロード
    if not glob.glob("*.zip"):
        Downloader(args.url)()

    if args.mode == "sample":
        """サンプルデータを用いて評価を実行"""
        Evaluator(args.sample_path, args.exe_path)()

    elif args.mode == "real":
        """実データを用いて評価を実行"""
        # Excelファイルを読み取る
        element, constraint = ExcelLoader(args.excel_path)()

        # 設計変数の種類数  var_len=222
        var_len = len(element.iloc[:, [0]])

        # 多目的最適化を行う
        answer = MultiOptim(element, constraint)(args.population_size, var_len, args)

        # もしevalディレクトリが無ければ作成
        os.makedirs("./eval", exist_ok=True)

        # 回答ファイルを作成
        with open("./eval/pop_vars_eval.txt", "w") as f:
            lines = ""
            for j in range(var_len):
                tmp = answer[0].variables[j]
                lines += str(tmp) + "\t"  # 列はタブで区切る
            # 末尾の\tを削除、改行を追加
            f.writelines(lines[:-1] + "\r\n")

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
        help="モード(sample:サンプルデータ、real:実データ)",
    )
    parser.add_argument(
        "--excel_path",
        type=str,
        default="./Mazda_CdMOBP/Info_Mazda_CdMOBP.xlsx",
        help="データが包含されたExcelファイルのパス名",
    )
    parser.add_argument(
        "--population_size",
        type=int,
        default=48,
        help="世代数",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        choices=["NSGAII", "SMPSO"],
        default="NSGAII",
        help="最適化アルゴリズム",
    )

    args = parser.parse_args()

    main(args)


# データ読み込み(サンプルコード)：回答記述方法を確認するために作成
# import csv
# with open("./Mazda_CdMOBP/Mazda_CdMOBP/sample/pop_vars_eval.txt") as f:
#     reader = csv.reader(f, delimiter='\t')
#     for row in reader:
#         for i in range(len(row)):
#             row[i]=row[i].replace(" ","")
#         print(row)
