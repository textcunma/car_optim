from deap import base
from deap import creator
from deap import tools
from deap import algorithms


def multioptim(element, constraint):
    """
    多目的最適化を行うメソッド
    目的関数1: 総重量(最小化)
    目的関数2: 共通部品数(最大化)

    :param element: 設計変数222個(74部品 x 3車種)存在
        [0] Initial (初期値) (呼び出し方):element_initial=element.iloc[:, [0]]
        [1] Lower Bound (下限値)
        [2] Upper Bound (上限値)
        [3] Design Space (設計空間??)
        [4] Discrete Volume (離散値範囲)
    :param constraint: 制約条件54種類
        [0] 1つ目の条件
        [1] 2つ目の条件
        ....
    """
    pass
