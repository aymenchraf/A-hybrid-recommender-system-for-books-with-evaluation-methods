import itertools
from surprise import accuracy


class RecommenderMetrics:

    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)

    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=False)

    def additionalMetrices(self ,rankings,TestData,simsAlgo,ratingThreshold=4.0):

      coverage_hits = 0
      usersCount=0
      n_diversity = 0
      total_diversity = 0
      n_novelty = 0
      total_novelty = 0

      for userID in TestData.keys() :
              
              topN = []

              predictions = [self.algorithm.predict(uid, iid, r_ui_trans)
                            for (uid, iid, r_ui_trans) in TestData[userID]]

              for userID, bookID, actualRating, estimatedRating, _ in predictions:
                  topN.append((int(bookID), estimatedRating))

              topN.sort(key=lambda x: x[1], reverse=True) 
              topN = topN[:10]

              # calculating coverage

              hit = False
              if (topN is not []) and (topN [0][1] >= ratingThreshold):
                      hit = True
              if (hit):
                      coverage_hits += 1
              
              #calculating diversty
              pairs = itertools.combinations(topN, 2)
              for pair in pairs:
                      book1 = pair[0][0]
                      book2 = pair[1][0]
                      innerID1 = simsAlgo.trainset.to_inner_iid(str(book1))
                      innerID2 = simsAlgo.trainset.to_inner_iid(str(book2))
                      similarity = simsAlgo.similarities[innerID1,innerID2]
                      total_diversity += similarity
                      n_diversity += 1

              #calculating novelty
              for rating in topN:
                      bookID = rating[0]
                      rank = rankings[bookID]
                      total_novelty += rank
                      n_novelty += 1
              usersCount+=1
              
      coverty = coverage_hits / usersCount
      diversity = (1 - (total_diversity / n_diversity))
      novelty= total_novelty / n_novelty
      return (coverty,diversity,novelty)