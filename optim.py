from platypus import NSGAII, Problem, Real, nondominated
import matplotlib.pyplot as plt


class MultiOptim:
    """
    多目的最適化を行うメソッド
    目的関数1: 総重量(最小化)
    目的関数2: 共通部品数(最大化)
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
    
    def __call__(self):
        def objective(vars):    # vars -> len=222
            return sum(vars)

        var_len=len(self.element.iloc[:, [0]])

        # 222変数2目的の問題
        # problem = Problem(var_len, 2)

        # 222変数1目的の問題
        problem = Problem(var_len, 1)

        # 最小化、最大化を設定
        # problem.directions[0] = Problem.MINIMIZE
        # problem.directions[1] = Problem.MAXIMIZE
        problem.directions[:] = Problem.MINIMIZE

        # 制約条件を設定
        problem.constraints[:] = "<0"   # 0未満ならばペナルティ

        design_var=[]
        for i in range(var_len):
            element=self.element.iloc[:, [4]].iloc[i][0].split(",")
            element=[float(x) for x in element]
            design_var.append(Real(element))    # Realは魔改造(Type.pyの内部コードをいじっている)

        # 決定変数の範囲を設定
        problem.types[:] = design_var

        # 目的関数を設定
        problem.function = objective

        # アルゴリズムを設定し, 探索実行
        algorithm = NSGAII(problem, population_size=50)
        algorithm.run(1000)

        # 非劣解をとりだす
        nondominated_solutions = nondominated(algorithm.result)
        for i in nondominated_solutions[0].variables:
            print(i)

        # グラフを描画
        # plt.scatter([s.objectives[0] for s in nondominated_solutions if s.feasible],
        #         [s.objectives[1] for s in nondominated_solutions if s.feasible])
        # plt.show()
        # print()