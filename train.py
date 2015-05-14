
# Click Fraud Classifier.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC

def meanSig(A):
  m1 = np.mean(A[:,0]); s1 = np.std(A[:,0])
  m2 = np.mean(A[:,1]); s2 = np.std(A[:,1])
  m3 = np.mean(A[:,2]); s3 = np.std(A[:,2])
  m4 = np.mean(A[:,3]); s4 = np.std(A[:,3])
  return [m1,m2,m3,m4,s1,s2,s3,s4]

trnX = np.genfromtxt("trnSet.dat")[:,1:]
m = meanSig(trnX)  # Get the mean and std. dev. for the Training set.
trnY = []
for i in range(0,len(trnX)):
  trnX[i][0] = (trnX[i][0]-m[0])/m[4]
  trnX[i][1] = (trnX[i][1]-m[1])/m[5]
  trnX[i][2] = (trnX[i][2]-m[2])/m[6]
  trnX[i][3] = (trnX[i][3]-m[3])/m[7]
  trnY.append(trnX[i][4])  
trnX = trnX[:,:4]  

cl = SVC(kernel="rbf", probability=True).fit(trnX,trnY)

tstX = np.genfromtxt("testSet.dat")
tstY = []
for i in range(0,len(tstX)):
  tstX[i][0] = (tstX[i][0]-m[0])/m[4]
  tstX[i][1] = (tstX[i][1]-m[1])/m[5]
  tstX[i][2] = (tstX[i][2]-m[2])/m[6]
  tstX[i][3] = (tstX[i][3]-m[3])/m[7]
  tstY.append(tstX[i][4])
tstX = tstX[:,:4]

L = len(tstY)
for threshold in [val/100. for val in range(0,101)]:

  tp = 0; tn = 0; fp = 0; fn = 0; one = 0; zero = 0
  for i in range(0,len(tstX)):
    pred = cl.predict_proba(tstX[i])[0]
    if pred[1] > threshold: 
      predicted = 1  # Not Fraud.
    else: predicted = 0

    if tstY[i] == 1 and predicted == 1: tp += 1
    if tstY[i] == 0 and predicted == 0: tn += 1  
    if tstY[i] == 0 and predicted == 1: fp += 1
    if tstY[i] == 1 and predicted == 0: fn += 1
    
    if tp == 0.: 
      precision = 0.; recall = 0.; F1 = 0.
    else:  
      precision = float(tp)/(tp+fp)
      recall = float(tp)/(tp+fn)
      F1 = 2.*float(tp)/((2.*tp)+fp+fn)
    
    if predicted == 1: one += 1
    else: zero += 1
    
  print threshold,tp,tn,fp,fn,precision,recall,F1,one,zero    
