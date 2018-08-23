#!/usr/bin/env python
#
# Kalman filter Library for using the Grove - Barometer (High-Accuracy)(http://www.seeedstudio.com/depot/Grove-Barometer-HighAccuracy-p-1865.html
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this library?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
# This library is derived from the Arduino library written by Oliver Wang for SeeedStudio (https://github.com/Seeed-Studio/Grove_Barometer_HP20x/tree/master/HP20x_dev)
from random import randint
Rand_Table=[
0.5377,1.8339,-2.2588,0.8622,0.3188,-1.3077,-0.4336,0.342,3.5784, 
2.7694,-1.3499,3.0349,0.7254,-0.0631,0.7147,-0.2050,-0.1241,1.4897, 
1.4090,1.4172,0.6715,-1.2075,0.7172,1.6302,0.4889,1.0347,0.7269, 
-0.3034,0.2939,-0.7873,0.8884,-1.1471,-1.0689,-0.8095,-2.9443,1.4384, 
0.3252,-0.7549,1.3703,-1.7115,-0.1022,-0.2414,0.3192,0.3129,-0.8649, 
-0.0301,-0.1649,0.6277,1.0933,1.1093,-0.8637,0.0774,-1.2141,-1.1135, 
-0.0068,1.5326,-0.7697,0.3714,-0.2256,1.1174,-1.0891,0.0326,0.5525, 
1.1006,1.5442,0.0859,-1.4916,-0.7423,-1.0616,2.3505,-0.6156,0.7481, 
-0.1924,0.8886,-0.7648,-1.4023,-1.4224,0.4882,-0.1774,-0.1961,1.4193, 
0.2916,0.1978,1.5877,-0.8045,0.6966,0.8351,-0.2437,0.2157,-1.1658, 
-1.1480,0.1049,0.7223,2.5855,-0.6669,0.1873,-0.0825,-1.9330,-0.439, 
-1.7947]
class KalmanFilter:
	X_pre=0
	X_post=0
	P_pre=0 
	P_post=0
	K_cur=0
	
	def __init__(self):
		self.X_pre=0
		
	def Gaussian_Noise_Cov(self):
		index = 0
		tmp=[0.0]*10
		average = 0.0
		sum = 0.0
		
		#Get random number */
		for i in range(10): 
		
			index = randint(0,90)
			tmp[i] = Rand_Table[index]
			sum += tmp[i];	
		
		# Calculate average
		average = sum/10
		
		#Calculate Variance 
		Variance = 0.0	
		for j in range(10):
			Variance += (tmp[j]-average)*(tmp[j]-average)
		Variance/=10.0	
		return Variance
		
	def Filter(self,origin):
		modelNoise = 0.0
		observeNoise = 0.0
		
		# Get model and observe Noise 
		modelNoise = self.Gaussian_Noise_Cov()
		observeNoise = self.Gaussian_Noise_Cov()
		
		# Algorithm 
		self.X_pre = self.X_post
		self.P_pre = self.P_post + modelNoise;
		self.K_cur = self.P_pre/(self.P_pre + observeNoise);
		self.P_post = (1 - self.K_cur)*self.P_pre;
		self.X_post = self.X_pre + self.K_cur*(origin - self.X_pre);
		
		return self.X_post