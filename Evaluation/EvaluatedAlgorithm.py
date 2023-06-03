from collections import defaultdict
from Evaluation.Metrics import RecommenderMetrics


class EvaluatedAlgorithm:
    
    def __init__(self, algorithm, name):
        self.algorithm = algorithm
        self.name = name
        
    def Evaluate(self, evaluationData, n=10, verbose=True):
        metrics = {}
        # Compute accuracy
        if (verbose):
            print("Evaluating accuracy of " + self.name + "  ...")

        self.algorithm.fit(evaluationData.GetTrainSet())
        predictions = self.algorithm.test(evaluationData.GetTestSet())

        metrics["RMSE"] = RecommenderMetrics.RMSE(predictions)
        metrics["MAE"] = RecommenderMetrics.MAE(predictions)

        if (verbose):
              print("Evaluating additional metrics for " + self.name + "  ...")

        self.algorithm.fit(evaluationData.GetFullTrainSet())
        antiTestSet= evaluationData.GetFullAntiTestSet()

        users = defaultdict(list)
        for uid, iid, r_ui_trans in antiTestSet:
          users[uid].append((uid, iid, r_ui_trans))    

        metrics["Coverage"],metrics["Diversity"],metrics["Novelty"]=RecommenderMetrics.additionalMetrices(self
                                                                                                          ,TestData=users
                                                                                                          ,rankings=evaluationData.GetPopularityRankings()
                                                                                                          ,simsAlgo=evaluationData.GetSimilarities())                                         
        if (verbose):
            print("Analysis complete.")

        return metrics
 
    def GetName(self):
        return self.name
    
    def GetAlgorithm(self):
        return self.algorithm