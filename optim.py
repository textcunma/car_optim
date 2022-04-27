"""
GNU Lesser General Public License v3.0
(C) DEAP
参考:https://github.com/DEAP/deap/blob/master/examples/ga/nsga2.py
"""
import array
import random
import numpy as np
from deap import base
from deap import creator
from deap import tools
from deap import benchmarks
from deap.benchmarks.tools import hypervolume


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

        # -------------------------------------------------
        random.seed(1)

        NGEN = 250  # 繰り返し世代数
        MU = 100  # 集団内の個体数
        CXPB = 0.9  # 交叉率

        # 世代ループ中のログに何を出力するかの設定
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        # 第一世代の生成
        pop = self.toolbox.population(n=MU)
        pop_init = pop[:]
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop = self.toolbox.select(pop, len(pop))

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(invalid_ind), **record)
        print(logbook.stream)

        # 最適計算の実行
        for gen in range(1, NGEN):
            # 子母集団生成
            offspring = tools.selTournamentDCD(pop, len(pop))
            offspring = [self.toolbox.clone(ind) for ind in offspring]

            # 交叉と突然変異
            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                # 交叉させる個体を選択
                if random.random() <= CXPB:
                    # 交叉
                    self.toolbox.mate(ind1, ind2)

                # 突然変異
                self.toolbox.mutate(ind1)
                self.toolbox.mutate(ind2)

                # 交叉と突然変異させた個体は適応度を削除する
                del ind1.fitness.values, ind2.fitness.values

            # 適応度を削除した個体について適応度の再評価を行う
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # 次世代を選択
            pop = self.toolbox.select(pop + offspring, MU)
            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(logbook.stream)

        # 最終世代のハイパーボリュームを出力
        print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))

        return pop, pop_init, logbook

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
            gene = [0] * n  # 遺伝子リスト
            for i in range(n):
                rangelist = list(self.element.iloc[:, [4]].iloc[i])
                gene[i]=random.choice(rangelist)   # 範囲リストからランダム選択
            return gene

        # 遺伝子を生成する関数を設定
        self.toolbox.register("attr_float", uniform, NDIM)

        # 個体を生成する関数を設定
        self.toolbox.register(
            "individual", 
            tools.initIterate, 
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
            low=0.0,        ### ????
            up=1.0,         ### ????
            eta=20.0
        )

        # 変異関数を設定
        self.toolbox.register(
            "mutate",
            tools.mutPolynomialBounded,
            low=0.0,        ### ???
            up=1.0,         ### ???
            eta=20.0,
            indpb=1.0 / NDIM,
        )

        # 個体選択法(NSGA-Ⅱ)を設定
        self.toolbox.register("select", tools.selNSGA2)
