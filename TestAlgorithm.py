from Algorithms.ContentBased import CBAlgorithm
from Algorithms.HybridBased import HybridAlgorithm
from Algorithms.KNNmBased import CoAlgorithm
from Algorithms.SGDBased import SGDAlgorithm
from DataProvider import DataProvider
from Evaluation.Evaluator import Evaluator
from surprise import NMF
from surprise import NormalPredictor
from surprise import KNNBasic


def LoadBooksAndRatingsData():
    BD = DataProvider()
    print("Loading book ratings...")
    data = BD.loadData()
    #computing book popularity ranks so we can measure novelty later
    rankings = BD.getPopularityRanks()
    return (BD, data , rankings)

#now lets use it
(BD , data  , rankings) = LoadBooksAndRatingsData()

evaluator = Evaluator(data, rankings)


CoRecommender  = CoAlgorithm()

CBRecommender  = CBAlgorithm()

SGDRecommender = SGDAlgorithm()

HybridRecommender = HybridAlgorithm ([CoRecommender,CBRecommender,SGDRecommender])

evaluator.AddAlgorithm(HybridRecommender, "HybridRecommender")

#standar NMF now
standardNMF = NMF(n_epochs=20,n_factors=20)
evaluator.AddAlgorithm(standardNMF, "NMF")

# KNNBasic
standardClustering = KNNBasic()
evaluator.AddAlgorithm(standardClustering, "KNNBasic")

# Just make random recommendations
Random = NormalPredictor()
evaluator.AddAlgorithm(Random, "Random")

# Test !
evaluator.Evaluate()