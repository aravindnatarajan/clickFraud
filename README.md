# clickFraud
Classifier to detect click fraud with online Ads.

Click fraud classification
using data from http://palanteer.sis.smu.edu.sg/fdma2012/

Extracted 4 features from the data:

1.  Number of clicks / Number of unique IP addresses.
2.  Number of clicks / Number of unique devices.
3.  Maximum number of clicks in a 5 second interval.
4.  Fraction of URL's with a null string.

SVM classifier with a gaussian kernel 
F1 score 77%

