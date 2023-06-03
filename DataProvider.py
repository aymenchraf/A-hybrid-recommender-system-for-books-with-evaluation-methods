import csv
import os
import sys
from surprise import Dataset, Reader
from collections import defaultdict

class DataProvider:
    bookID_to_name = {}
    name_to_BookID = {}
    ratingsPath = 'data/5K_users_ratings.csv'
    booksPath = 'data/books_data.csv'

    def loadData(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.bookID_to_name = {}
        self.name_to_BookID = {}

        reader = Reader( sep=',', skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.booksPath, newline='', encoding='UTF-8') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)  # Skip header line
            for row in bookReader:
                bookID = int(row[0])
                bookName = row[1]
                self.bookID_to_name[bookID] = bookName
                self.name_to_BookID[bookName] = bookID
        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                userID = int(row[0])
                if (user == userID):
                    book_id = int(row[1])
                    rating = float(row[2])
                    userRatings.append((book_id, rating))

        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                bookID = int(row[1])
                ratings[bookID] += 1
        rank = 1
        for bookID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[bookID] = rank
            rank += 1
        return rankings

    def getGenres(self):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)  # Skip header line
            for row in bookReader:
                bookID = int(row[0])
                genreList = [x.strip('[] ') for x in row[5].split(',')]
                genreIDList = []
                for genre in genreList:
                    if genre in genreIDs:
                        genreID = genreIDs[genre]
                    else:
                        genreID = maxGenreID
                        genreIDs[genre] = genreID
                        maxGenreID += 1
                    genreIDList.append(genreID)
                genres[bookID] = genreIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (bookID, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[bookID] = bitfield
        return genres

    def getYears(self):
        years = defaultdict(int)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)
            for row in bookReader:
                bookID = int(row[0])
                year = int(row[3])
                if year:
                    years[bookID] = year
        return years

    def getStandardGeners(self):
        geners = defaultdict(list)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)
            for row in bookReader:
                bookID = int(row[0])
                bookGeners = row[5].split(',')
                for gener in bookGeners :
                  geners[bookID].append(gener)
        return geners

    def getAuthors(self):
        authors = defaultdict(list)
        with open(self.booksPath, newline='', encoding='ISO-8859-1') as csvfile:
            bookReader = csv.reader(csvfile)
            next(bookReader)
            for row in bookReader:
                bookID = int(row[0])
                authors[bookID]=[x.strip('[] ') for x in row[2].split(',')]
        return authors

    def getBookName(self, bookID):
        if bookID in self.bookID_to_name:
            return self.bookID_to_name[bookID]
        else:
            return ""

    def getBookID(self,bookName):
        if bookName in self.name_to_BookID:
            return self.name_to_BookID[bookName]
        else:
            return 0