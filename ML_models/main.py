# -*- coding: utf-8 -*-
"""ML_Models

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oCjqvE2K4TWVskJwsNvxHWIhcZCYwqR8
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

cols = ["fLength","fWidth","fSize" ,"fConc","fConc1","fAsym","fM3Long","fM3Trans","fAlpha","fDist","class"]
df= pd.read_csv("magic04.data",names=cols)

df["class"] =  (df["class"]=="g").astype(int)

for label in cols[:-1]:
  plt.hist(df[df["class"]==1][label],color="blue",label="gamma",alpha=0.7,density=True)
  plt.hist(df[df["class"]==0][label],color="red",label="hadron",alpha=0.7,density=True)
  plt.title(label)
  plt.ylabel("Probability")
  plt.xlabel(label)
  plt.legend()
  plt.show()

train,valid,test = np.split(df.sample(frac=1),[int(0.6*len(df)),int(0.8*len(df))])

def scale_dataset(dataframe,oversample=False):
  x = dataframe[dataframe.columns[:-1]].values
  y = dataframe[dataframe.columns[-1]].values

  scaler = StandardScaler()
  x = scaler.fit_transform(x)

  if oversample:
    ros = RandomOverSampler()
    x,y= ros.fit_resample(x,y)

  data = np.hstack((x,np.reshape(y,(-1,1))))

  return data,x,y

train,X_train,Y_train =  scale_dataset(train,oversample=True)
valid,X_valid,Y_valid =  scale_dataset(valid,oversample=False)
test,X_test,Y_test =  scale_dataset(test,oversample=False)

"""KNN Model"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train,Y_train)
y_pred = knn_model.predict(X_test)
print(classification_report(Y_test,y_pred))

"""Naive-Bayes Model"""

from sklearn.naive_bayes import GaussianNB

nb_model = GaussianNB()
nb_model.fit(X_train,Y_train)
y_pred = nb_model.predict(X_test)
print(classification_report(Y_test,y_pred))

"""SVM Model"""

from sklearn.svm import SVC

svm_model = SVC()
svm_model.fit(X_train,Y_train)
y_pred = svm_model.predict(X_test)
print(classification_report(Y_test,y_pred))

"""Log Regression Model"""

from sklearn.linear_model import LogisticRegression

log_reg_model = LogisticRegression()
log_reg_model.fit(X_train,Y_train)
y_pred = log_reg_model.predict(X_test)
print(classification_report(Y_test ,y_pred))

"""Neural Networks

"""

import tensorflow as tf

def plot_history(history):
  fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
  ax1.plot(history.history['loss'], label='loss')
  ax1.plot(history.history['val_loss'], label='val_loss')
  ax1.set_xlabel('Epoch')
  ax1.set_ylabel('Binary crossentropy')
  ax1.grid(True)

  ax2.plot(history.history['accuracy'], label='accuracy')
  ax2.plot(history.history['val_accuracy'], label='val_accuracy')
  ax2.set_xlabel('Epoch')
  ax2.set_ylabel('Accuracy')
  ax2.grid(True)


  plt.show()

def train_model(X_train,Y_train,num_nodes,dropout_prob,lr,batch_size,epoch):
  nnet_model = tf.keras.Sequential([
      tf.keras.layers.Dense(num_nodes, activation='relu', input_shape=(10,)),
      tf.keras.layers.Dropout(dropout_prob),
      tf.keras.layers.Dense(num_nodes, activation='relu'),
      tf.keras.layers.Dropout(dropout_prob),
      tf.keras.layers.Dense(1, activation='sigmoid')
  ])

  nnet_model.compile(optimizer=tf.keras.optimizers.Adam(lr), loss='binary_crossentropy', metrics=['accuracy'])
  history = nnet_model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=0)
  return nnet_model,history

least_val_loss = float('inf')
least_loss_model = None
epochs = 100

for num_nodes in [16,32,64]:
  for dropout_prob in [0,0.2]:
    for lr in [0.01,0.005,0.001]:
      for batch_size in [32,64,128]:
        print(f"{num_nodes} num_nodes, {dropout_prob} dropout_prob, {lr} lr, {batch_size} batch_size")
        nnet_model, history = train_model(X_train,Y_train,num_nodes,dropout_prob,lr,batch_size,epochs)
        plot_history(history)
        val_loss = nnet_model.evaluate(X_valid,Y_valid)[0]
        if val_loss < least_val_loss:
          least_val_loss = val_loss
          least_loss_model = nnet_model

y_pred = least_loss_model.predict(X_test)
y_pred = (y_pred > 0.5).astype(int).reshape(-1,)
print(classification_report(Y_test,y_pred))