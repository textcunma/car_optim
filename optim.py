"""
GNU Lesser General Public License v3.0
(C) DEAP
https://github.com/DEAP/deap
"""
import array
import random
import numpy as np
from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap import algorithms


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

        # Toolboxの作成(進化演算に必要)
        self.toolbox = base.Toolbox()

    def __call__(self):
        # 基本設定を行う
        self.setting()

        #---------------------------------
        # 参考：https://darden.hatenablog.com/entry/2017/04/18/225459
        random.seed(42)

        pop = self.toolbox.population(n=300)

        hof = tools.HallOfFame(1, similar=np.array_equal)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=40, stats=stats,halloffame=hof)

        return pop, stats, hof


    def setting(self):
        """基本設定を行うメソッド"""
        # 目的関数を設定 weights=(1.0,-1.0) ==> 最大化 & 最小化の意味
        creator.create("MultiFitness", base.Fitness, weights=(1.0, -1.0))

        # 個体クラスを作成  typecode='d' ==> double型
        creator.create(
            "Individual", array.array, typecode="d", fitness=creator.MultiFitness
        )

        # 遺伝子数を設定    遺伝子数 = 設計変数 の数???
        NDIM = len(self.element.iloc[:, [0]])

        # 最大値と最小値をnumpyで設定
        lower=np.array(self.element.iloc[:, [1]])
        upper=np.array(self.element.iloc[:, [2]])

        # サンプルコード↓
        # 遺伝子生成メソッド
        # def uniform(low,up,size):
        #     try:
        #         a=[random.uniform(a, b) for a, b in zip(low, up)]
        #         return a
        #     except TypeError:
        #         a=[random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]
        #         return a
        #
        # self.toolbox.register("attr_float", uniform, 0.0,1.0,NDIM)

        # 遺伝子生成関数
        def uniform(n):
            """
            param: n: 遺伝子数
            """
            
            gene = np.empty(n)  # 遺伝子numpy配列
            for i in range(n):
                rangelist = list(self.element.iloc[:, [4]].iloc[i])
                gene[i]=random.choice(rangelist)   # 範囲リストからランダム選択
            return gene

        # 遺伝子を生成する関数を設定
        self.toolbox.register("attr_float", uniform, NDIM)

        # 個体を生成する関数を設定
        self.toolbox.register(
            "individual", 
            np.ndarray,
            creator.Individual,
            self.toolbox.attr_float
        )

        # 世代を作成する関数を設定
        self.toolbox.register(
            "population", 
            tools.initRepeat, 
            list, 
            self.toolbox.individual
        )

        # 評価関数(目的関数)を設定
        self.toolbox.register("evaluate", benchmarks.zdt1)

        # 交叉関数を設定
        self.toolbox.register(
            "mate", 
            tools.cxSimulatedBinaryBounded, 
            low=lower,        ### どうかな????
            up=upper,         ### どうかな????
            eta=20.0
        )

        # 変異関数を設定
        self.toolbox.register(
            "mutate",
            tools.mutPolynomialBounded,
            low=lower,        ### どうかな???
            up=upper,         ### どうかな???
            eta=20.0,
            indpb=1.0 / NDIM,
        )

        # 個体選択法(NSGA-Ⅱ)を設定
        self.toolbox.register("select", tools.selNSGA2)
