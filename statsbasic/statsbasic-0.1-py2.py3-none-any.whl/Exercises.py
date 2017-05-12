import numpy as np
import pandas as pd
import statsbasic as sdt

#############################2016 exam
#1)
sdt.T_test_OneSample(2.9, 2.6, 0.4, 36, 0.05)

sdt.T_test_OneSample(2.9, 2.85, 0.0989, 36, 0.05)

#if it was divide by 4, not 16:
sdt.T_test_OneSample(2.9, 2.85, np.sqrt(0.1565/4), 36, 0.05)

#2)
data = np.array([
    ['','Men','Woman'],
    ['Rare',39,40],
    ['Often',61,60]
])
dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
sdt.ChiSquare_test(dfObs, debug=True)

####ORRR 
data = np.array([
    ['','W-Rare','W-Often'],
    ['M-Rare',24,15],
    ['M-Often',16,46]
])
dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
sdt.ChiSquare_test(dfObs, debug=True)


 #3)
    
labels = ['OI', 'OE', 'YI', 'YE']
data =[[.38, .38,.43,.51,.54,.57,.62,.59,.65,.78,.93,.79,.51,.76],
       [.98,.93,.92,1.02,.89,.88,.86,.41,.44,.54,.58,.63,.67,.71],
       [.36,.4,.3,1.17,.84,.68,.23,.11,.48,.13,.32,.14,.11,.16],
       [1.11, 1.25,1.56,1.54,.42,.37,.41,.26,.83,.52,.83,.2,.33,.27]]

dfObs = sdt.CreateAnovaDataFrame(labels, data)
sdt.AnovaOneWay(dfObs)
    

#############################2015 Exam
#1)
sdt.T_test_TwoDependentSamples(0.637, 0.237, 6, 0.05)
sdt.T_test_TwoDependentSamples(0.55, 0.117, 5, 0.05)
sdt.T_test_TwoInDependentSamples(89.272, 89.908, 0.553, 0.364, 6, 6, 0.05)

#2)
labels = ['A', 'B', 'C', 'D']
data =[[13.9, 13.9,12.7,14.3,13.3,14,14,14.5,13.4,13.2,13.8],
       [15.4,16.9,16.7,16.6,16.2,17.3,19.1,18.4,17.4,18,18.2],
       [13.5,14.9,14.5,16.1,14.4,16.5,15.6,14.9,13.9,14.5,14.5],
       [17.9,17.2,16.5,18,17.7,17.1,17.6,18.1,18.8,18.4,17.9]]

dfObs = sdt.CreateAnovaDataFrame(labels, data)
sdt.AnovaOneWay(dfObs)



#3)
data = np.array([
    ['','Ireland','France'],
    ['18-24',112,163],
    ['25-39',176,297],
    ['40-54',185,263],
    ['50+',100,97]
])
dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
sdt.ChiSquare_test(dfObs, debug=True)


############################2014 Exam
#1)
sdt.T_test_TwoInDependentSamples(36.16, 39.73, 5.07, 6.22,  10, 10, 0.05)

sdt.T_test_TwoDependentSamples(3.57, 4.15**2, 10, 0.05, 'two')


#2)
labels = ['12', '24', '36', '48']
data =[[3,6,3,3,1,2,2,2],
       [4,5,4,3,2,3,4,3],
       [7,8,7,6,5,6,5,6],
       [7,8,9,8,10,10,9,11]]

dfObs = sdt.CreateAnovaDataFrame(labels, data)
#stats.f_oneway(data[0],data[1],data[2],data[3])
sdt.AnovaOneWay(dfObs)



#3)
data = np.array([
    ['','Glan','Bal','Par'],
    ['Not Germinated',405,341,252],
    ['Germinated',386,180,39]
])

data = np.array([
    ['','Glan','Bal'],
    ['Not Germinated',405,341],
    ['Germinated',386,180]
])
dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
sdt.ChiSquare_test(dfObs, debug=True)


############################2013 Exam
#1)
#a) 
sdt.T_test_OneSample(14, 14.3, 0.8, 25, 0.05)
#b) 
sdt.T_test_OneSample(14, 16.4, 0.75, 25, 0.05)
# c and d)
sdt.T_test_TwoInDependentSamples(14.3, 16.4, 0.8, 0.75, 25,25,0.05)

#2)
data = np.array([
    ['','Ireland','France'],
    ['T',71,109],
    ['P',324,499],
    ['N',178,212]    
])
dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
sdt.ChiSquare_test(dfObs, debug=True)

#c)
    
n1 = 573
n2 = 720
pYes1 = 0.31
pYes2 = 0.425
#Question does not give us the pYesTotal, so we have to calculate it
pYesTotal = ((pYes1 * n1) + (pYes2 * n2)) / (n1 +n2)

sdt.CountData_TwoInDependentSamples(pYes1, pYes2, pYesTotal, n1, n2, 0.05)
    
    
#3)
labels = ['C', 'LD', 'HD']
data =[[0.228, 0.207, 0.234, 0.220, 0.217, 0.228, 0.209, 0.221, 0.204, 0.220, 0.203, 0.219, 0.218, 0.245, 0.210],
       [0.211, .220, .211,.233,.219,.233,.226,.228,.216,.225,.200,.208,.198, .208,.203],       
       [.25,.237,.217,.206,.247,.228,.245,.232,.267,.261,.221,.219,.232,.209,.255]]

dfObs = sdt.CreateAnovaDataFrame(labels, data)
#stats.f_oneway(data[0],data[1],data[2],data[3])
sdt.AnovaOneWay(dfObs)
    
reload(sdt)
#Chapter 2 Suplementary Exercises:
    
#1) 
sdt.T_test_OneSample(200, 195.62, 5.62, 30, 0.05)

#2)s(xbar_sample_diffs, S_sample_diffs, n , alpha, tail = 'two', direction = 'none'):
sdt.T_test_TwoDependentSamples(1.518, 1.580, 11, 0.05)

#3) 
sdt.T_test_TwoDependentSamples(37, 1071, 20, 0.05)
    
#3)def T_test_TwoInDependentSamples(xbar_A, xbar_B, StDev_A, StDev_B, nA, nB, alpha, tail = 'two', direction = 'none'):
    
sdt.T_test_TwoInDependentSamples(105.84, 111.06, 14.27, 11.89, 31,31,0.05)

sdt.T_test_TwoInDependentSamples(105.84, 110.96, 14.27, 12.12, 31,47,0.05)





#1)