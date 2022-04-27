from asyncio import constants
import pandas as pd
import argparse


class ExcelLoader:
    """Excelファイルからデータを読み取る"""

    def __init__(self, excel_path):
        self.excel_path = excel_path

    def __call__(self):
        excel_data = pd.ExcelFile(self.excel_path)  # Excelファイルを読み取る
        sheet_name = excel_data.sheet_names  # シート名を取得
        excel_df = excel_data.parse(sheet_name[1])  # シート名を指定してデータを読み取る
        element = excel_df.iloc[7:229,3:8]  # 部品情報(7行~228行、D列~H列)を取得
        constraint = excel_df.iloc[6:229,11:65]  # 制約条件(7行~228行、L列~BM列)を取得
        element_initial=element.iloc[:, [0]]
        element_lower_bound=element.iloc[:, [1]]
        element_upper_bound=element.iloc[:, [2]]
        element_design_space=element.iloc[:, [3]]
        element_discrete_vol=element.iloc[:, [4]]
        print(element_discrete_vol)

def main(args):
    """
    クラスの挙動を確認するための試験的メソッド
    """
    ExcelLoader(args.excel_path)()  # Excelファイルを読み取る


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="メインスクリプト")
    parser.add_argument(
        "--excel_path",
        type=str,
        default="./Mazda_CdMOBP/Info_Mazda_CdMOBP.xlsx",
        help="データが包含されたExcelファイルのパス名",
    )
    args = parser.parse_args()
    main(args)
