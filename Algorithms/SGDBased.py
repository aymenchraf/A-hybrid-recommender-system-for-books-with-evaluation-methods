import surprise
import numpy as np
from surprise import AlgoBase, PredictionImpossible

# also extended from an empty recommender template called "AlgoBase"
class SGDAlgorithm(AlgoBase):

    def __init__(self, learning_rate=0.01, n_epochs=20, n_factors=20, reg=0.02):
        #initialize the hyperparameters
        self.learning_rate = learning_rate
        self.n_epochs = n_epochs
        self.n_factors = n_factors
        self.reg = reg

    def fit(self, trainset):
        #fitting the trainingset
        AlgoBase.fit(self, trainset)

        # initialize user and item factors , p for users , q for items
        self.users_f = np.random.normal(scale=1.0/self.n_factors, size=(self.trainset.n_users, self.n_factors))
        self.books_f = np.random.normal(scale=1.0/self.n_factors, size=(self.trainset.n_items, self.n_factors))

        # iterate over epochs and optimize factors using SGD
        for _ in range(self.n_epochs):
            for userID, bookID, rating in self.trainset.all_ratings():
                error = rating - np.dot(self.users_f[userID], self.books_f[bookID])
                #correcting the error in user and item factors
                self.users_f[userID] += self.learning_rate*(error*self.books_f[bookID]-self.reg*self.users_f[userID])
                self.books_f[bookID] += self.learning_rate*(error*self.users_f[userID]-self.reg*self.books_f[bookID])
        
    
    #the most important fonction .. 
    #we calculate the estimate Rating between a user and an item
    #the built in function "predict" will use this function later
    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User or item is unknown.')

        #the estimated rating is the dot bettwen item and user learned factors
        est = np.dot(self.users_f[u], self.books_f[i])

        return est
        
    #to predict all estimated ratings of a user
    def EstamedRatingsForUser(self,u):
        prid = []
        for item in range(self.trainset.n_items):     
              rating = self.predict(str(u) , str(self.trainset.to_raw_iid(item)))
              prid.append(rating)

        return prid
    