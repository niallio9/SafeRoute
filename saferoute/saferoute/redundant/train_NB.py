#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 13:43:16 2019

@author: niall
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

# Import the dataset
df = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_clean_with_roads.csv')
df = df[df['collision_count'] > 0]
df_synthetic = pd.read_csv('/Users/niall/insight_project/data/cleaned/collision_events_synthetic_with_roads.csv')
df_synthetic.columns = df.columns
df = df.append(df_synthetic, ignore_index=True)
del df_synthetic
df_top = df.head()

features = ['longitude', 'latitude',
       'street_type_1', 'road_class', 'visibility', 'collision_type',
       'impact_type', 'light', 'road_surface_cond', 'year', 'month',
       'day_of_week', 'hour_of_day','collision_count']
features_cat = ['road_class', 'visibility', 'light',
                'road_surface_cond', 'year', 'month', 'day_of_week', 'hour_of_day']
#features_cat = ['highway']
X = df[features_cat]
y = df['collision']

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import make_column_transformer
preprocessor = make_column_transformer( (OneHotEncoder(), features_cat), remainder="passthrough")
X = preprocessor.fit_transform(X)
#X = X.toarray()

#from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#enc = OneHotEncoder(handle_unknown='ignore')
#enc.fit(X)
#X = enc.transform(X)

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import MultinomialNB
model = MultinomialNB()
model.fit(X_train, y_train)
xtest_prob = model.predict_proba(X_test) # can use this method to get P(X|Y)

## Fitting Decision Tree Classification to the Training set
#from sklearn.tree import DecisionTreeClassifier
#classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
#classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = model.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# save the model to disk
filename = 'model_NB.sav'
pickle.dump(model, open(filename, 'wb'))
filename_transformer = 'feature_encoder.sav'
pickle.dump(preprocessor, open(filename_transformer, 'wb'))

