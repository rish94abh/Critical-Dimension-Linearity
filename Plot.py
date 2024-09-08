# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt

price=[2.5, 1.23, 3.2,6.4,1.9]
sale=[3,6,3,1,7]
CSVdata=open('data.csv')
2DArray=np.genfromtxt(CSVdata, delimiter=',')
plt.scatter(price,sale)
plt.show()
