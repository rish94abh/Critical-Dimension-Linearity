#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 22:20:10 2022

@author: rishabhkushwaha
"""
from scipy import signal
from math import pi, exp , sqrt
import numpy as np
import matplotlib.pyplot as plt

#Define Variables
PSF_size=41
End_Pt=int(PSF_size/2)
sigma_CDSEM=2
sigma_eSL10=10
CDSEM_PSF=np.zeros(PSF_size)
eSL10_PSF=np.zeros(PSF_size)

time=np.arange(1,10001)
CDSEM_Th=90
eSL10_Th=90
Diff=np.zeros((19,500))
eSL10_CD=np.zeros((19,40))
SEM_CD=np.zeros(40)
slope=np.zeros((19,500))
Input_CD=np.zeros(40)
Low_Lim=np.zeros(40)
Hi_Lim=np.zeros(40)
signal_Input=np.zeros((40,10000))
signal_eSL10=np.zeros((40,10000))
signal_CDSEM=np.zeros((40,10000))
#Generating PSF
for x in range(-1*End_Pt,1+End_Pt):
    CDSEM_PSF[x+End_Pt] = exp(-(float((x)**2))/(2*(sigma_CDSEM**2)))/((100*sigma_CDSEM)*sqrt(2*pi))
    eSL10_PSF[x+End_Pt] = exp(-(float((x)**2))/(2*(sigma_eSL10**2)))/((100*sigma_eSL10)*sqrt(2*pi))   

#Generating multiple input instances
for Iterations in range(0,500):
    
    
    Input=np.zeros(40)
    eSL10_left=0
    CDSEM_left=0
    
    #Generating Input
    Low_Lim[Iterations]=np.random.randint(10,20)
    "Input_CD[Iterations]=np.random.randint(5, 50-Low_Lim[Iterations])"
    Input_CD[Iterations]=np.random.randint(5, 15)
    Hi_Lim[Iterations]=Low_Lim [Iterations] + Input_CD[Iterations]
    Input[int(Low_Lim[Iterations]):int(Hi_Lim[Iterations])]=1
    
    
    #Computing Output signal by convolving input with PSF
    CDSEM=signal.fftconvolve(Input, CDSEM_PSF, mode='same')
    eSL10=signal.fftconvolve(Input, eSL10_PSF, mode='same')
    CDSEM=np.amax(eSL10)*CDSEM/(np.amax(CDSEM))
    #Storing input values
    signal_Input[Iterations]=Input
    signal_eSL10[Iterations]=eSL10
    signal_CDSEM[Iterations]=CDSEM
    
    
    #Estimating CDSEM edges at given Edge threshold
    #Temp=np.amax(CDSEM)*CDSEM_Th/100
    #for i in range(int(Low_Lim[Iterations]-200*sigma_CDSEM),int(Low_Lim[Iterations]+200*sigma_CDSEM)):
     #   if(CDSEM[i]<=Temp<=CDSEM[i+1]):
      #      CDSEM_left=i+(Temp-CDSEM[i])/(CDSEM[i+1]-CDSEM[i])
       #     SEM_CD[Iterations]=Input_CD[Iterations]+2*(Low_Lim[Iterations]-CDSEM_left)
    
    #Estimating Edge placement for CDSEM and eSL10
    for eSL10_Th in range(4,19):
        Temp=np.amax(eSL10)*eSL10_Th*5/100
        for i in range(int(Low_Lim[Iterations]-200*sigma_eSL10),int(Low_Lim[Iterations]+200*sigma_eSL10)):
            if(eSL10[i]<=Temp<=eSL10[i+1]):
                eSL10_left=i+(Temp-eSL10[i])/(eSL10[i+1]-eSL10[i])
                eSL10_CD[eSL10_Th][Iterations]=Input_CD[Iterations]+2*(Low_Lim[Iterations]-eSL10_left)
            if(CDSEM[i]<=Temp<=CDSEM[i+1]):
                #CDSEM_left=i
                CDSEM_left=i+(Temp-CDSEM[i])/(CDSEM[i+1]-CDSEM[i])
                SEM_CD[Iterations]=Input_CD[Iterations]+2*(Low_Lim[Iterations]-CDSEM_left)
                
    
        #Calculating error between CDSEM and eSL10 at different eSL10 thresholds
        Diff[eSL10_Th][Iterations]= CDSEM_left-eSL10_left

#Plot Results
#plt.plot(time,Orig, label='Input')  
#plt.plot(time,CDSEM, label='CDSEM')
#plt.plot(time,eSL10, label='eSL10')
model=np.zeros((5,2))
i=0
y=SEM_CD/100
plt.plot(SEM_CD/100, SEM_CD/100,'.')
for eSL10_Th in range(8,18,2):
    plt.plot(SEM_CD/100,eSL10_CD[eSL10_Th]/100,'.', label=5*eSL10_Th) 
#    model[i]=np.polyfit(SEM_CD/100, eSL10_CD[eSL10_Th]/100,1)
#    plt.plot(SEM_CD/100, eSL10_CD[eSL10_Th]/100)
    i=i+1
plt.xlabel('CDSEM_CD')
plt.ylabel('eSL10_CD')
plt.legend()

del CDSEM, CDSEM_PSF, CDSEM_Th, CDSEM_left 
del eSL10, eSL10_PSF, eSL10_Th, eSL10_left, Temp, Input, Low_Lim, Hi_Lim, Iterations, time,x, PSF_size,End_Pt, Input_CD
del sigma_CDSEM, sigma_eSL10, i