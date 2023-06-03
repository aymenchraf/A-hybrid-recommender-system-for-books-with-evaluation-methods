#we use the famous KNN algorithm as one of our recommenders
#we dont need to code the hole algo because its on ready exist in suprise lib as "KNNWithMeans"
import surprise
from surprise import KNNWithMeans


class CoAlgorithm(KNNWithMeans):
  def __init__(self, k=40):
        #init the algorithm , we want the CF user-user not item-item
        KNNWithMeans.__init__(self,sim_options={'name': 'cosine','user_based': True})
        self.k = k

  #fitting the trainset into the algoerithm
  #the fit function of KNNWithMeans has on ready a fonction "compute similarity" built in
  #so we dont need to write one

  def fit(self,trainset):
        #fiting the data
        KNNWithMeans.fit(self,trainset)
        

  #every algorithm has a function called "pridect" 
  #that uses another function called "estimate" that generate the predicted rating      
  #the estimate function are on ready built in , so we dont need to define it in this algo
  #on other algorithms, we will define it


  #the predict function generate a rating between one user and one item
  #to predict all estimated ratings of a user i create this function
  
  def EstamedRatingsForUser(self,u):
        prid = []
        for item in range(self.trainset.n_items):
              
              rating = self.predict(str(u) , str(self.trainset.to_raw_iid(item)))
              prid.append(rating)

        return prid

