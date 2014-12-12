#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      krossa
#
# Created:     09/12/2014
# Copyright:   (c) krossa 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''Imports'''
import numpy as np
import scipy as sp                                                                    # NumPy used for creating arrays

from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.optimize import fsolve

import matplotlib
import matplotlib.pyplot as plt
import pylab

##def func (x, a, b, c, d):
##    return d + c/(1+np.exp(a-b*x))

def func (x, p10, p11, p12, p13, p14, p15):
    return p10+ (p11*( 1./(1 + np.exp(p12*(x-p13)))) + (1./(1+np.exp(-p14*(x-p15)))  - 1 ))
##    0.1000 + (0.9000*( 1./(1+ np.exp(0.5000*(x-90)))) + (1./(1+np.exp(-0.5000*(x-200)))  - 1 ))

x = [90, 97,104,111,125,132,139,146,153,160,167,174,181,188,195,202,209,216,223,230,237,244,251,258,265,272,279]
y = [0.1957, 0.2061,0.2718,0.2729,0.4398,0.4672,0.1054,0.5947,0.677,0.74,0.6936,0.6416,0.7221,0.7219,0.7653,0.7869,0.721,0.68,0.5787,0.5891,0.1054,0.4672,0.4398,0.2729,0.2718,0.2061,0.1957]

newX = np.linspace(1,300,300)

popt = np.empty((6))
p0 =  (0.1000, 0.9000, 0.5000, 90, 0.5000, 200)

try:
            popt, pcov = curve_fit(func, x, y, p0)

except RuntimeError:
            print("Error - curve_fit failed")


ndviSOS = 0.45

p10=popt[0]
p11=popt[1]
p12=popt[2]
p13=popt[3]
p14=popt[4]
p15=popt[5]

Log2 = lambda x: (p10+ (p11*( 1./(1 + np.exp(p12*(x-p13)))) + (1./(1+np.exp(-p14*(x-p15)))  - 1 )))-ndviSOS
SOSrange=np.array([100,200])
result2 = fsolve(Log2,SOSrange)
print result2

#Plot
pylab.plot(newX,func(newX,*popt),result2,Log2(result2),'go')
pylab.plot(newX,func(newX,*popt),x,y,'ro')
pylab.grid(b=1)
pylab.show()