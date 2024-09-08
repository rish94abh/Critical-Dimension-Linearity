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
PSF_size=5001
End_Pt=int(PSF_size/2)
sigma_CDSEM=1
sigma_eSL10=7
model=np.zeros((5,2))

intercept=np.zeros(9)
for sigma_eSL10 in range(1,6,1):
    slope=np.zeros(500)
    CDSEM_PSF=np.zeros(PSF_size)
    eSL10_PSF=np.zeros(PSF_size)
    
    time=np.arange(1,10000)
    CDSEM_Th=40
    eSL10_Th=50
    Diff=np.zeros((19,500))
    eSL10_CD=np.zeros((19,500))
    SEM_CD=np.zeros(500)
    Input_CD=np.zeros(500)
    Low_Lim=np.zeros(500)
    Hi_Lim=np.zeros(500)
    
    #Generating PSF
    for x in range(-1*End_Pt,1+End_Pt):
        CDSEM_PSF[x+End_Pt] = exp(-(float((0.01*x)**2))/(2*((sigma_CDSEM)**2)))/((100*sigma_CDSEM)*sqrt(2*pi))
        eSL10_PSF[x+End_Pt] = exp(-(float((0.01*x)**2))/(2*((0.5*sigma_eSL10)**2)))/((100*0.5*sigma_eSL10)*sqrt(2*pi))   
    
    #Generating multiple input instances
    for Iterations in range(0,500):
        
        
        Input=np.zeros(10000)
        eSL10_left=0
        CDSEM_left=0
        
        #Generating Input
        Low_Lim[Iterations]=np.random.randint(3000,5000)
        "Input_CD[Iterations]=np.random.randint(5, 50-Low_Lim[Iterations])"
        Input_CD[Iterations]=np.random.randint(500, 1500)
        Hi_Lim[Iterations]=Low_Lim [Iterations] + Input_CD[Iterations]
        Input[int(Low_Lim[Iterations]):int(Hi_Lim[Iterations])]=1
        
        
        #Computing Output signal by convolving input with PSF
        CDSEM=signal.fftconvolve(Input, CDSEM_PSF, mode='same')
        eSL10=signal.fftconvolve(Input, eSL10_PSF, mode='same')
        
        #Estimating CDSEM edges at given Edge threshold
        Temp=np.amax(CDSEM)*CDSEM_Th/100
        for i in range(int(Low_Lim[Iterations]-200*sigma_CDSEM),int(Low_Lim[Iterations]+200*sigma_CDSEM)):
            if(CDSEM[i]<=Temp<=CDSEM[i+1]):
                CDSEM_left=i+(Temp-CDSEM[i])/(CDSEM[i+1]-CDSEM[i])
                #CDSEM_left=i
                SEM_CD[Iterations]=Input_CD[Iterations]+2*(Low_Lim[Iterations]-CDSEM_left)
        
        #Estimating Edge placement for CDSEM and eSL10
        for eSL10_Th in range(4,19):
            Temp=np.amax(eSL10)*eSL10_Th*5/100
            for i in range(int(Low_Lim[Iterations]-200*sigma_eSL10),int(Low_Lim[Iterations]+200*sigma_eSL10)):
                if(eSL10[i]<=Temp<=eSL10[i+1]):
                    eSL10_left=i+(Temp-eSL10[i])/(eSL10[i+1]-eSL10[i])
                    #eSL10_left=i
                    eSL10_CD[eSL10_Th][Iterations]=Input_CD[Iterations]+2*(Low_Lim[Iterations]-eSL10_left)
                if(CDSEM[i]<=Temp<=CDSEM[i+1]):
                    CDSEM_left=i
                    
        
            #Calculating error between CDSEM and eSL10 at different eSL10 thresholds
            Diff[eSL10_Th][Iterations]= CDSEM_left-eSL10_left
    
    #Plot Results
    #plt.plot(time,Orig, label='Input')  
    #plt.plot(time,CDSEM, label='CDSEM')
    #plt.plot(time,eSL10, label='eSL10')
    
    #model[i]=np.polyfit(SEM_CD/100, eSL10_CD[9]/100,1)
    #plt.plot(SEM_CD/100,eSL10_CD[10]/100,'.', label=sigma_eSL10)
    #s=int((sigma_eSL10-1)/3)
    #SEM_CD.sort()
   # p=eSL10_CD[10]
   # p.sort()
    #p=0
   # for s in range(1,499):
      #  if(SEM_CD[s+1]-SEM_CD[s] > 0):
     #       slope[p]=(eSL10_CD[10][p+1]-eSL10_CD[10][p])/(SEM_CD[p+1]-SEM_CD[p])
    #        p=p+1
    #slope[s],intercept[s]=np.polyfit(np.log(SEM_CD/100), np.log(eSL10_CD[10]/100), 1)
    #plt.plot(SEM_CD/100,slope,'.', label=sigma_eSL10)
    #i=i+1
    
    plt.scatter(SEM_CD/100,eSL10_CD[12]/100, label=sigma_eSL10) 

plt.xlabel('CDSEM_CD')
plt.ylabel('eSL10_CD')
plt.legend()

