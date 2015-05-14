
#   Mining for features.
#   Data from http://palanteer.sis.smu.edu.sg/fdma2012/

"""
An example: 
[0: '9794476', 
 1: '1071324855', 
 2: 'SonyEricsson_K70', 
 3: 'dv3va', 
 4: 'dsfag', 
 5: 'us', 
 6: '2012-03-08 00:00:00.0', 
 7: 'ad', 
 8: '\n']
"""

"""
ad: Adult Sites
co: Community
es: Entertainment/Lifestyle
gd: Glamor/Dating
in: Information
mc: Mobile content
pp: Premium portal
se: Search service
"""

import numpy as np
import sys

#theDay = 23
#pubFile   = "publishers_23feb12.csv"
#clickFile = "clicks_23feb12.csv"
#lookForFraud = True

#theDay = 9
#pubFile   = "publishers_09feb12.csv"
#clickFile = "clicks_09feb12.csv"
#lookForFraud = False

theDay = 8
pubFile   = "publishers_08mar12.csv"
clickFile = "clicks_08mar12.csv"
lookForFraud = True

lines = len([val for val in open(pubFile, "r").readlines()])-1
f_pub = open(pubFile, "r")
A = f_pub.readline() 
fr = []; nof = []
for i in range(0,lines):
  A = f_pub.readline()  
  status = A.split(",")[-1][:-1] 
  ip = A.split(",")[0]
  if status != "OK" and status != "Fraud": continue
  if status == "OK":     nof.append(ip)
  if status == "Fraud":  fr.append(ip)
f_pub.close()


timeStep = 5.   # number of clicks from the same device in a 5 second period.
lines = len([val for val in open(clickFile, "r").readlines()])-1
if lookForFraud: num = len(fr)
else: num = len(nof)


for st in range(10,num):
  for lp in range(st,st+1):
    f_clicks  = open(clickFile, "r")
    A = f_clicks.readline()  

    if lookForFraud: publisher = fr[lp]
    else:            publisher = nof[lp]
    allIP = []; ref = []
  
    uniqueIP = {}; uniqueDevice = {}  
    first = True
    ref = []
    clicks = 0; oldD = 0; oldDevice = ""
    theMax = 0
    content = {'ad':0, 'co':0, 'es':0, 'gd':0, 'in':0, 'mc':0, 'pp':0, 'se':0 }
    ii = 0; cc = 0; bb = 0; pp = 0
    for i in range(0,lines):
      A = f_clicks.readline().split(",")  
      theIP = A[1]; theDevice = A[2]; 
      thePublisher = A[3]; theCountry = A[5]; theDate = A[6]
      theContent = A[7]; theRef = A[8]; 
      
      # Change day:hour:minutes:seconds to a number.
      dateNum = ((int(theDate[9])-theDay)*24.) + (int(theDate[11])*10.+int(theDate[12])*1.) + ((int(theDate[14])*10.+int(theDate[15])*1.)/60.) + ((int(theDate[17])*10.+int(theDate[18])*1.)/3600.)    

      if thePublisher == publisher:            
        if theCountry == 'in': ii += 1
        if theCountry == 'cn': cc += 1        
        if theCountry == 'bn': bb += 1                
        if theCountry == 'pk': pp += 1                        
        if not first:
          if dateNum - oldD < timeStep and A[2] == oldDevice : 
            ctr += 1
          else:
            if ctr > theMax: theMax = ctr
            ctr = 1
            oldD = dateNum; oldDevice = A[2]
      
        clicks += 1
        if first: 
          first = False        
          oldD = dateNum; oldDevice = A[2]; ctr = 1
          dateNum0 = dateNum

        ref.append(theRef)                
        if theContent in content: content[theContent] += 1
        if theIP not in uniqueIP: uniqueIP[theIP] = 1
        else: uniqueIP[theIP] += 1
        if theDevice not in uniqueDevice: uniqueDevice[theDevice] = 1
        else: uniqueDevice[theDevice] += 1
        
  ll = len([val for val in ref if val == "\n"])
  print lp,clicks,len(uniqueIP), len(uniqueDevice), (float(clicks)/len(uniqueIP)), (float(clicks)/len(uniqueDevice)),ll/float(clicks), theMax, (ii+cc+bb+pp)/float(clicks)
  #print (float(clicks)/len(uniqueIP)), (float(clicks)/len(uniqueDevice)),ll/float(clicks), theMax, " 0"  
  #print clicks,ii,cc
