# -*- coding: utf-8 -*-
"""Spam_Detection (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dN5YbRf5kRZofPggOMJgncHoRN4TxxKd
"""

import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')

data = pd.read_csv("/content/Spam Email raw text for NLP.csv", encoding='latin-1')

data.head()

data.drop('FILE_NAME', axis = 1, inplace = True)

data

data.CATEGORY.value_counts()

stopword = nltk.corpus.stopwords.words('english')

lemmatizer = WordNetLemmatizer()

corpus = []

for i in range(len(data)):
  # Remove all non-aplhanumeric characters
  messages = re.sub('[^a-zA-Z0-9]', ' ', data['MESSAGE'][i])

  # Convert to lower case
  messages = messages.lower()

  # Split into words for lemmetization
  messages = messages.split()

  # Remove stopwords and lemmatizing
  messages = [lemmatizer.lemmatize(word) for word in messages
              if word not in set(stopwords.words('english'))]

  # Convert words back to sentences
  messages = ' '.join(messages)

  # Adding preprocessed data into corpus
  corpus.append(messages)

cv = CountVectorizer(max_features = 2500, ngram_range = (1,3))
X = cv.fit_transform(corpus).toarray()
y = data.CATEGORY

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 1, stratify = y)

tf = TfidfVectorizer(ngram_range = (1,3), max_features = 2500)
X = tf.fit_transform(corpus).toarray()

import pickle
pickle.dump(tf, open('cv.pkl', 'wb'))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 1, stratify = y)

model = MultinomialNB()

model.fit(X_train, y_train)

train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

print(classification_report(train_pred, y_train))
print(classification_report(test_pred, y_test))

from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(y_test, test_pred)
score = accuracy_score(y_test,test_pred)
print(cm,score*100)

pickle.dump(model, open("spam.pkl", "wb"))

loaded_model = pickle.load(open("spam.pkl", "rb"))
loaded_model.predict(X_test)
loaded_model.score(X_test,y_test)

def new_review(new_review):
  new_review = new_review
  new_review = re.sub('[^a-zA-Z]', ' ', new_review)
  new_review = new_review.lower()
  new_review = new_review.split()
  lemmatizer = WordNetLemmatizer()
  new_review = [lemmatizer.lemmatize(word) for word in new_review
              if word not in set(stopwords.words('english'))]
  new_review = ' '.join(new_review)
  new_corpus = [new_review]
  new_X_test = cv.transform(new_corpus).toarray()
  new_X_test = tf.transform(new_corpus).toarray()
  new_y_pred = loaded_model.predict(new_X_test)

  return new_y_pred

new_review = new_review(str(input("Enter new review...")))
if new_review[0]==1:
  print("Spam")
else :
  print("Not spam")

print('Predicting...')

message = ["You won 10000 dollars, please provide your account details,So that we can transfer the money"]

message_vector = tf.transform(message)
category = model.predict(message_vector)
print("The message is", "spam" if category == 1 else "not spam")

