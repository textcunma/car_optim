import subprocess

class Evaluator():
    def __init__(self,input_path,exe_path):
        """
        :param input_path: 評価用入力ファイルのパス名
        :param exe_path: 評価時の実行ファイル(mazda_mop.exe)パス名
        """
        self.input_path=input_path
        self.exe_path=exe_path
    
    def __call__(self):
        subprocess.call(self.exe_path+" "+self.input_path)
        print("Complete Evaluation")