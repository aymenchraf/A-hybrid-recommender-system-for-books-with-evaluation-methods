
from Evaluation.EvaluationData import EvaluationData
from Evaluation.EvaluatedAlgorithm import EvaluatedAlgorithm


class Evaluator:
    
    algorithms = []
    
    def __init__(self, dataset, rankings):
       
        ed = EvaluationData(dataset, rankings)
        print("done...")
        self.dataset = ed
        
    def AddAlgorithm(self, algorithm, name):
        alg = EvaluatedAlgorithm(algorithm, name)
        self.algorithms.append(alg)
        
    def Evaluate(self):
        results = {}
        for algorithm in self.algorithms:
            print("Evaluating ", algorithm.GetName(), "...")
            results[algorithm.GetName()] = algorithm.Evaluate(self.dataset)

        # Print results
        print("{:<10} {:<10} {:<10}{:<10} {:<10} {:<10}".format("Algorithm", "RMSE", "MAE", "Coverage", "Diversity", "Novelty"))
        for (name, metrics) in results.items():
             print("{:<10} {:<10.4f} {:<10.4f}{:<10.4f} {:<10.4f} {:<10.4f}".format(name, metrics["RMSE"], metrics["MAE"],metrics["Coverage"], metrics["Diversity"], metrics["Novelty"]))
                
        print("metrics:\n")
        print("RMSE:      Root Mean Squared Error. Lower values mean better accuracy.")
        print("MAE:       Mean Absolute Error. Lower values mean better accuracy.")
        print("Coverage:  Ratio of users for whom recommendations above a certain threshold exist. Higher is better.")
        print("Diversity: 1-S, where S is the average similarity score between every possible pair of recommendations")
        print("           for a given user. Higher means more diverse.")
        print("Novelty:   Average popularity rank of recommended items. Higher means more novel.")