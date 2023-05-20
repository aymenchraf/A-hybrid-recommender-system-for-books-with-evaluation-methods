# A-hybrid-recommender-system-for-books-with-evaluation-methods

This is a hybrid book recommendation system, based on three sub-recommendation systems:  content based, KNNm based and SGD based. With code for evaluate the performance.

This repository contains the python codes that were developed during my preparation for the master's graduation thesis, which was entitled: "Designing a Hybrid Book Recommendation System". You can demand the access to a copy of it from here:  .

About the used dataset: 
We have used the dataset in this repository : https://github.com/zygmuntz/goodbooks-10k.
We have modified the books.csv file where we kept the important columns in it,With all books preserved. And, we renamed it to newBooks.csv .
As for the ratings.csv file, we have created more than one version to suit the experimental environment. You can choose between these files as per your convenience: 5K_users_ratings.csv, 10K_users_ratings.csv, 20K_users_ratings.csv.
I do not recommend using a file with many users during the evaluation process, because this will require a lot of RAM and time.

How to use:
This code can be tested as  or as a Python notebook.

You can try the code a Python file through the following steps:
1. Run the requirements file to install the necessary libraries.
2. Change the ratings file used according to the environment you are going to use. Go to the file and change the name of the file in the line.
3. The recommendation system can be used to generate lists of recommendations through the file: .
4. The performance of the hybrid recommendation system or any other recommendation system built with the Surprise library can be evaluated through the file: .

You can try the code a Python notebook through the following steps:
1. Upload the file to Google Colab or any similar environment.
2. Create a new folder named "data", and upload the CSV files to it.
3. Run it!

If there are any errors or suggestions, please let me know. Thanks!
