"""
GNU Lesser General Public License v3.0
(C) DEAP
参考:https://github.com/DEAP/deap/blob/master/examples/ga/nsga2.py
"""

import random
from deap import base
from deap import creator
from deap import tools
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

        self.toolbox = base.Toolbox()
    
    def __call__(self):
        pass

    
    def setting(self):
        """基本設定を行うメソッド"""
        # 目的関数を設定 weights=(1.0,-1.0) ==> 最大化 & 最小化の意味
        creator.create("Fitness", base.Fitness, weights=(1.0,-1.0))

        # 遺伝子数を設定
        NDIM = 30


        def uniform(low, up, size=None):
            try:
                return [random.uniform(a, b) for a, b in zip(low, up)]
            except TypeError:
                return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]
