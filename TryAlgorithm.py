from Algorithms.HybridBased import HybridAlgorithm 
from Algorithms.KNNmBased import CoAlgorithm
from Algorithms.ContentBased import CBAlgorithm
from Algorithms.SGDBased import SGDAlgorithm
from DataProvider import DataProvider


def LoadBooksAndRatingsData():
    BD = DataProvider()
    print("Loading book ratings...")
    data = BD.loadData()
    #computing book popularity ranks so we can measure novelty later
    trainset = data.build_full_trainset()
    rankings = BD.getPopularityRanks()
    return (BD, trainset , rankings)

#now lets use it
(BD , data, rankings) = LoadBooksAndRatingsData()

CoRecommender  = CoAlgorithm()

CBRecommender  = CBAlgorithm()

SGDRecommender = SGDAlgorithm()

Recommender = HybridAlgorithm ([CoRecommender,CBRecommender,SGDRecommender])

Recommender.fit(data)
while True:
    user= str(input("please select a user, select 0 to end the programme:"))
    if user == "0":
        break
    try:
        data.to_inner_uid(user)
    except:
        print("invalid user.")
        continue

        #get this user ratings
    userRatings = BD.getUserRatings(int(user))
    loved = []
    hated = []
    ratings_that_exist = []
    for ratings in userRatings:
        #to elemenate this books from recommendations later
        ratings_that_exist.append(ratings[0])

        if (float(ratings[1]) >= 4.0):
            loved.append(ratings)
        elif float(ratings[1]) < 3.0:
            hated.append(ratings)

    print("\nUser ", user , " loved these books:")
    for ratings in loved:
        print(BD.getBookName(int(ratings[0]))+" | with rating :"+ str(ratings[1]) + " | geners :"+str(BD.getStandardGeners()[int(ratings[0])]))
    print("\n...and didn't like these books:")
    for ratings in hated:
        print(BD.getBookName(int(ratings[0]))+" | with rating :"+ str(ratings[1]) + " | geners :"+str(BD.getStandardGeners()[int(ratings[0])]))
    Predictions = Recommender.EstamedRatingsForUser(user)
    #lets convert this data to recommendations
    recommendations = []
    for uid, iid, r_ui, est, details in Predictions :
                    intBookID = int(iid)
                    if intBookID not in ratings_that_exist: # to elemenate books that alerdy readed
                        recommendations.append((intBookID, est))

    #top ratings first
    recommendations.sort(key=lambda x: x[1], reverse=True) 
    print ("\nWe recommend:")     
    for ratings in recommendations[:10]:
        print(BD.getBookName(ratings[0])+ " | Estamed rating : "+ str(ratings[1])+ " | geners :"+str(BD.getStandardGeners()[int(ratings[0])])+ " | year : "+str(BD.getYears()[int(ratings[0])])+" | authors : "+str(BD.getAuthors()[int(ratings[0])]))