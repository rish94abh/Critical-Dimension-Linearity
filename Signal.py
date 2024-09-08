#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 18:59:57 2022

@author: rishabhkushwaha
"""
from scipy import signal
from math import pi, exp , sqrt
import numpy as np
import matplotlib.pyplot as plt

#Define Variables
PSF_size=5001
End_Pt=int(PSF_size/2)
sigma_CDSEM=2
sigma_eSL10=7
match=0
CDSEM_PSF=np.zeros(PSF_size)
eSL10_PSF=np.zeros(PSF_size)

time=np.arange(1,10001)
CDSEM_Th=40
#eSL10_Th=10
Diff=np.zeros(19)
eSL10_CD=np.zeros(19)
SEM_CD=np.zeros(10000)
Input_CD=np.zeros(10000)
Low_Lim=np.zeros(10000)
Hi_Lim=np.zeros(10000)

#Generating PSF
for x in range(-1*End_Pt,1+End_Pt):
    CDSEM_PSF[x+End_Pt] = exp(-(float((0.01*x)**2))/(2*(sigma_CDSEM**2)))/(100*(sigma_CDSEM)*sqrt(2*pi))
    eSL10_PSF[x+End_Pt] = exp(-(float((0.01*x)**2))/(2*(sigma_eSL10**2)))/(100*(sigma_eSL10)*sqrt(2*pi))   
    
#Generating multiple input instances
    
    
Input=np.zeros(10000)
eSL10_left=0
CDSEM_left=0

#Generating Input
Low_Lim=3000
"np.random.randint(10,20)"
Input_CD=np.random.randint(5000,6000)
Hi_Lim=Low_Lim  + Input_CD
Input[Low_Lim:Hi_Lim]=1


#Computing Output signal by convolving input with PSF
CDSEM=signal.fftconvolve(Input, CDSEM_PSF, mode='same')
eSL10=signal.fftconvolve(Input, eSL10_PSF, mode='same')
eSL10=np.amax(CDSEM)*eSL10/(np.amax(eSL10))
#Estimating CDSEM edges at given Edge threshold
Temp=np.amax(CDSEM)*CDSEM_Th/100
for i in range(int(Low_Lim-2*sigma_CDSEM),int(Low_Lim+2*sigma_CDSEM)):
    if(CDSEM[i]<=Temp<=CDSEM[i+1]):
        SEM_CD=Input_CD+2*(Low_Lim-i)

#Estimating Edge placement for CDSEM and eSL10
for eSL10_Th in range(4,19):
    Temp=np.amax(eSL10)*eSL10_Th*5/100
    for i in range(Low_Lim-2*sigma_eSL10,Low_Lim+2*sigma_eSL10):
        if(eSL10[i]<=Temp<=eSL10[i+1]):
            eSL10_left=i
            eSL10_CD[eSL10_Th]=Input_CD+2*(Low_Lim-i)
        if(CDSEM[i]<=Temp<=CDSEM[i+1]):
            CDSEM_left=i
            

    #Calculating error between CDSEM and eSL10 at different eSL10 thresholds
    Diff[eSL10_Th]= CDSEM_left-eSL10_left

#Plot Results
plt.plot(time/100,Input, label='Input')  
plt.plot(time/100,CDSEM, label='CDSEM')
plt.plot(time/100,eSL10, label='eSL10')

for time in range(2000,4000):
        if(eSL10[time]==CDSEM[time]):
            match=eSL10[time]


#plt.scatter(eSL10,CDSEM)

plt.xlabel('Time(s)')
plt.ylabel('Signal')
plt.legend()