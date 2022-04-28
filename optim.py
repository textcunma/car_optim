from platypus import NSGAII, SMPSO, Problem, Real, nondominated
import time

class MultiOptim:
    """
    多目的最適化
    目的関数1: 総重量(最小化)
    ※ 目的関数2: 共通部品数(最大化) <== 今回は省略(実質、単目的最適化)
    """

    def __init__(self, element, constraint):
        """
        :param element: 設計変数222個(74部品 x 3車種)存在
            [0] Initial (初期値) (呼び出し方):element_initial=element.iloc[:, [0]]
            [1] Lower Bound (下限値)
            [2] Upper Bound (上限値)
            [3] Design Space (設計空間??)
            [4] Discrete Volume (離散値範囲)
        :param constraint: 制約条件54種類(値が0以上でなければペナルティ)
            [0] 1つ目の条件
            [1] 2つ目の条件
            ....
        """
        self.element = element
        self.constraint = constraint

    def __call__(self, population_size, var_len, args):
        # 目的関数(総和を最小化する)
        def objective(vars):  # vars -> len=222
            return sum(vars)

        # 222変数1目的の問題
        problem = Problem(var_len, 1)

        # 最小化を設定
        problem.directions[:] = Problem.MINIMIZE

        # 制約条件を設定(0以上でなければいけない)
        problem.constraints[:] = ">=0"

        design_var = []
        for i in range(var_len):
            element = self.element.iloc[:, [4]].iloc[i][0].split(",")
            element = [float(x) for x in element]
            # RealはType.pyの内部コードをいじっている（詳細は最下部）
            design_var.append(Real(element))

        # 設計変数の範囲を設定
        problem.types[:] = design_var

        # 目的関数を設定
        problem.function = objective

        # NSGA-Ⅱアルゴリズムを設定
        if args.algorithm == "NSGAII":
            algorithm = NSGAII(problem, population_size=population_size)
        elif args.algorithm == "SMPSO":
            algorithm = SMPSO(problem, population_size=population_size)
        
        # 実行
        sp=time.time()  # 開始時間
        algorithm.run(1000)
        gp=time.time()  # 終了時間
        print("algorithm:", args.algorithm, "time:", gp-sp,"[sec]")

        # パレート解を抽出
        nondominated_solutions = nondominated(algorithm.result)

        return nondominated_solutions


# 改造したRealクラスを以下に示す

# class Real(Type):
#     """Represents a floating-point value with min and max bounds.

#     Attributes
#     ----------
#     min_value : int
#         The minimum value (inclusive)
#     max_value: int
#         The maximum value (inclusive)
#     """

#     # def __init__(self, min_value, max_value):
#     def __init__(self, inputlist):
#         super(Real, self).__init__()
#         # self.min_value = float(min_value)
#         # self.max_value = float(max_value)
#         self.min_value = inputlist[0]
#         self.max_value = inputlist[-1]
#         self.DiscreteList = inputlist


#     def rand(self):
#         # return random.uniform(self.min_value, self.max_value)
#         return random.choice(self.DiscreteList)

#     def __str__(self):
#         # return "Real(%f, %f)" % (self.min_value, self.max_value)
#         return
