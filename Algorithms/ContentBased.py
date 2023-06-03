
from surprise import AlgoBase, PredictionImpossible
import heapq
import math
import numpy as np


from DataProvider import DataProvider


class CBAlgorithm(AlgoBase):

    def __init__(self, k=40, sim_options={}):
        AlgoBase.__init__(self)
        self.k = k

    def fit(self, trainset , load= False):
        #fiting the data
        AlgoBase.fit(self, trainset)

        # Load up metadata for every book
        BD = DataProvider()
        genres = BD.getGenres()
        years = BD.getYears()
        authors = BD.getAuthors()

        #if you have a copy od similarities 
        if load :
          self.similarities = self.importSimilarities()
          print("...done.")
          return self

        #generating sim distance for every book combination as a 2x2 matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))

        # to calculate it
        # Compute item similarity matrix based on content attributes
        print("Computing content-based similarity matrix...")
        for thisItem in range(self.trainset.n_items):
            if (thisItem % 100 == 0):
                #just to print the progress every 100 books so you wouldnt suicide
                print(thisItem, " of ", self.trainset.n_items)

            for otherItem in range(thisItem+1, self.trainset.n_items):
                #get the inner IDs
                thisBookID = int(self.trainset.to_raw_iid(thisItem)) 
                otherBookID = int(self.trainset.to_raw_iid(otherItem))

                #get the sub similarities
                genreSimilarity = self.computeGenreSimilarity(thisBookID, otherBookID, genres)
                if genreSimilarity == 0 :
                  sim = 0 
                else :
                  yearSimilarity = self.computeYearSimilarity(thisBookID, otherBookID, years)
                  authorSimilarity = self.computeAuthorSimilarity(thisBookID, otherBookID, authors)
                  sim = genreSimilarity * authorSimilarity * yearSimilarity
                  
                self.similarities[thisItem, otherItem] = sim
                self.similarities[otherItem, thisItem] = sim

        print("...done.")

    

    def computeGenreSimilarity(self, book1, book2, genres):
        #computing gener similarities with cosine way
        genres1 = genres[book1]
        genres2 = genres[book2]
        sumxx, sumxy, sumyy = 0, 0, 0
        for i in range(len(genres1)):
            x = genres1[i]
            y = genres2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
        
        return sumxy/math.sqrt(sumxx*sumyy)
    
    #compute year similarities .. this way is not good yet
    def computeYearSimilarity(self, book1, book2, years):
        diff = abs(years[book1] - years[book2])
        return math.exp(-0.007 *diff)



    #compute author similarities
    def computeAuthorSimilarity(self,book1, book2 , authors):
      total_similarities = 0
      authors1 = authors[book1]
      authors2 = authors[book2]
      total_elements = len(authors1) + len(authors2)

      for author1 in authors1:
          for author2 in authors2:
              if author1 == author2: # check if strings are exactly the same
                  total_similarities += 1
                  break
      
      similarity_percentage = (total_similarities / total_elements)*2 + 1
      return similarity_percentage

    def exportSimilarities(self):
        np.savetxt('/content/drive/MyDrive/data/CB-Similarities.txt',self.similarities)
          

    def importSimilarities(self):   
      return np.loadtxt('/content/drive/MyDrive/data/CB-Similarities.txt')

    #the most important fonction .. 
    #we calculate the estimate Rating between a user and an item
    #the built in function "predict" will use this function later
    def estimate(self, u, i):

        #making sure that the item and user exsit
        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')
        
        #creating the neighbors list of rated items by the users
        neighbors = []
        for rating in self.trainset.ur[u]:
            Similarity = self.similarities[i,rating[0]]
            neighbors.append( (Similarity, rating[1]) )

        #picking k neighbors
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])

        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if (simScore > 0):
                simTotal += simScore
                weightedSum += simScore * rating
            
        if (simTotal == 0):
            raise PredictionImpossible('No neighbors')
            
        predictedRating = weightedSum/simTotal
        return predictedRating
    
    #to predict all estimated ratings of a user
    def EstamedRatingsForUser(self,u):
      prid = []
      for item in range(self.trainset.n_items):     
            rating = self.predict(str(u) , str(self.trainset.to_raw_iid(item)))
            prid.append(rating)

      return prid
