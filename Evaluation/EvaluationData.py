from Algorithms.ContentBased import CBAlgorithm
from surprise.model_selection import train_test_split

class EvaluationData:
    
    def __init__(self, data, popularityRankings):
        
        self.rankings = popularityRankings
        
        #Build a full training set for evaluating overall properties
        self.fullTrainSet = data.build_full_trainset()
        self.fullAntiTestSet = self.fullTrainSet.build_anti_testset()
        
        #Build a 75/25 train/test split for measuring accuracy
        self.trainSet, self.testSet = train_test_split(data, test_size=.25, random_state=1)

        #Using our content based recommender to compute similarty matrix between items so we can measure diversity
        self.simsAlgo = CBAlgorithm()
        print("first, let's calculate similarities bettween books with our CB algorithm, so we can measure diversity later ..")
        self.simsAlgo.fit(self.fullTrainSet)
        
            
    def GetFullTrainSet(self):
        return self.fullTrainSet
    
    def GetFullAntiTestSet(self):
        return self.fullAntiTestSet
    
    def GetTrainSet(self):
        return self.trainSet
    
    def GetTestSet(self):
        return self.testSet   
    
    def GetSimilarities(self):
        return self.simsAlgo
    
    def GetPopularityRankings(self):
        return self.rankings