# -*- coding: utf-8 -*-
"""parkinson's Analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V_JYseCEh9HkSTIE5W5HI7lPPw3ZMN2a

Importing Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

"""Data"""

df = pd.read_csv("/content/parkinsons (1).data")

df.head

df.columns

df.describe

df.info()

df.isnull().sum()

df.shape

df['status'].value_counts()

import seaborn as sns
sns.countplot(df['status'])

df.dtypes

X = df.drop(['name'], 1)
X = X.drop(['status'], 1)
y = df['status']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))

X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
from sklearn.ensemble import VotingClassifier

# Create a Random Forest Classifier object
rfc = RandomForestClassifier(random_state=42)

# Fit the model to the training data
rfc.fit(X_train, y_train)

# Make predictions on the test data
rfc_predictions = rfc.predict(X_test)

# Calculate accuracy score of Random Forest Classifier
rfc_accuracy = accuracy_score(y_test, rfc_predictions)

# Create an XGBoost Classifier object
xgb = XGBClassifier(random_state=42)

# Fit the model to the training data
xgb.fit(X_train, y_train)

# Make predictions on the test data
xgb_predictions = xgb.predict(X_test)

# Calculate accuracy score of XGBoost Classifier
xgb_accuracy = accuracy_score(y_test, xgb_predictions)

# Create individual classifiers
log_clf = LogisticRegression()
svm_clf = SVC(probability=True)

# Create voting classifier with soft voting
voting_clf = VotingClassifier(
    estimators=[('lr', log_clf), ('svc', svm_clf)],
    voting='soft')

# Fit voting classifier on training data
voting_clf.fit(X_train, y_train)

# Make predictions on test data
predictions = voting_clf.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, predictions)

# Logistic Regression
lr = LogisticRegression()
lr.fit(X_train, y_train)
lr_predictions = lr.predict(X_test)
lr_accuracy = accuracy_score(y_test, lr_predictions)

# SVM
svm = SVC()
svm.fit(X_train, y_train)
svm_predictions = svm.predict(X_test)
svm_accuracy = accuracy_score(y_test, svm_predictions)

print("Random Forest Classifier Accuracy:", rfc_accuracy)
print("XGBoost Classifier Accuracy:", xgb_accuracy)
print("Logistic Regression Accuracy: ",lr_accuracy)
print("SVM Accuracy: ",svm_accuracy)

import pickle

# Writing different model files to file
with open( 'modelForPrediction.sav', 'wb') as f:
    pickle.dump(xgb,f)
    
with open('standardScalar.sav', 'wb') as f:
    pickle.dump(sc,f)

import matplotlib.pyplot as plt

# Accuracy scores
accuracy_scores = [lr_accuracy, svm_accuracy, rfc_accuracy, xgb_accuracy]

# Models names
model_names = ['Logistic Regression', 'SVM', 'Random Forest', 'XGBoost']

# Plot the bar chart
plt.bar(model_names, accuracy_scores, color=['orange', 'green', 'blue', 'red'])
plt.ylim(0.8, 1)
plt.ylabel('Accuracy')
plt.title('Model Accuracy Comparison')
plt.show()