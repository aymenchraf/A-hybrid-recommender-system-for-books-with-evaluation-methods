    
class HybridAlgorithm:
  def __init__(self, reommendersList):
    self.recommenders = reommendersList

  def fit(self, trainset):
    for algorithm in self.recommenders:
      algorithm.fit(trainset)
  def predict(self, uid, iid, r_ui=None, clip=True, verbose=False):
    predictions = []
    for algorithm in self.recommenders:
      predictions.append(algorithm.predict(uid, iid, r_ui, clip=True, verbose=False))
    mean = 0
    for uid, iid, r_ui, est, details in predictions :
      mean += est
    mean = mean/ len(predictions)
    prediction = [predictions[0][0],predictions[0][1],predictions[0][2], mean ,predictions[0][4]]
    return prediction
  def test(self, testset, verbose=False):
    predictions = [
            self.predict(uid, iid, r_ui_trans, verbose=verbose)
            for (uid, iid, r_ui_trans) in testset ]
    return predictions
  def EstamedRatingsForUser(self,u):
        prid = []
        for item in range(self.recommenders[0].trainset.n_items):     
              rating = self.predict(str(u) , str(self.recommenders[0].trainset.to_raw_iid(item)))
              prid.append(rating)

        return prid