from scipy import stats
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import operator
#http://www.graphpad.com/quickcalcs/

'''
Returns the T critical value at an alpha level
https://docs.scipy.org/doc/scipy/reference/tutorial/stats.html
'''
def GetT_Crit(alpha, df, tail, direction='none', debug=True):
    auxlabel =''
    if tail =='two':
        alpha = alpha /2
        auxlabel = '+-'
    elif tail == 'one':
        #just keeing this here to remmebr that the stats.t.ppf assumes one-tail 
        alpha = alpha # :)  no need to change alpha; 
          
    t_crit = stats.t.ppf(1-alpha, df)   
    if tail == 'one' and direction == 'lower':
        t_crit = t_crit * -1 # gets the negative end of the t-crit distribution
    
    t_crit = round(t_crit,2)
    if debug:
        print 't crit:', auxlabel +str(t_crit)
    return t_crit
    


def GetF_Crit(alpha, dfn, dfd, tail, direction='none', debug=True):      
    auxlabel =''
    if tail =='two':
        alpha = alpha /2
        auxlabel = '+-'
          
    f_crit =  stats.f.ppf(1-alpha, dfn,dfd) 
              
    if tail == 'one' and direction == 'lower':
        f_crit = f_crit * -1 # gets the negative end of the t-crit distribution
    
    f_crit = round(f_crit,2)
    if debug:
        print 'FCrit:', auxlabel +str(f_crit)
    return f_crit

def InterpretT_Stat(t_crit, t_stat, tail, direction='none'):
    if tail =='two':
        #if two tails; t-crit will always be positive because Im doing alpha -1
        if t_stat < t_crit * -1 or t_stat > t_crit:
            print 'Reject Ho'
        else:
            print 'Cannot reject Ho'
    elif tail == 'one':
        if direction == 'upper':
            if t_stat > t_crit:
                print 'Upper tail test; t-stat > t-crit : Reject Ho'
            else:
                print 'Upper tail test; t-stat < t-crit : Cannot Reject Ho'
        elif direction == 'lower':
            if t_stat < t_crit:
                print 'Lower tail test; t-stat < t-crit : Reject Ho'
            else:
                print 'Lower tail test; t-stat > t-crit : Cannot Reject Ho'
        else:
            print 'direction parameter has to be "upper" or "lower"'
    else:
        print 'tail parameter has to be "two" or "one"'


def CalculateCI(t_crit, x_bar, SE_xbar):
    #For the lower tail calculation, the tcrit is negative so the other calculations makes sense;    
    #Getting the absolute value of tcrit becaue the calculation bellow assumes it to be positive;
    t_crit = abs(t_crit)   
    
    #4) CI:
    CI_lower = round( x_bar - (t_crit * SE_xbar) , 3)
    CI_upper = round( x_bar + (t_crit * SE_xbar) , 3)
    print 'CI:',  [CI_lower, CI_upper]
    return CI_lower, CI_upper

    
def plotFDistribution(FCrit, FValue, dfModel, dfError):
    mu = 0
    x = np.linspace(0, FValue + 2, 1001)[1:]
    fig, ax = plt.subplots(figsize=(5, 3.75))
    dist = stats.f(dfModel, dfError, mu)
    plt.plot(x, dist.pdf(x), ls='-', c='black',
             label=r'$d_1=%i,\ d_2=%i$' % (dfModel, dfError))
    
    plt.xlim(0, FValue+2)
    plt.ylim(0.0, 1.0)
    

    plt.annotate('F Crit\n (%s)'%FCrit  , xy=(FCrit , 0), xytext=(FCrit-1, 0.4),arrowprops=dict( facecolor='red', shrink=0.05))
    plt.annotate('F Value\n (%s)'%FValue, xy=(FValue, 0), xytext=(FValue-2, 0.2), arrowprops=dict( facecolor='blue', shrink=0.05))
                
                
    plt.xlabel('$x$')
    plt.ylabel(r'$p(x|d_1, d_2)$')
    plt.title("Fisher's Distribution")
    
    plt.legend()
    plt.show()

def CreateAnovaDataFrame(labels, data):        
    dfObs = pd.DataFrame()
    i=0
    for d in data:
        dfObs[labels[i]] = d
        i+=1
    return dfObs
    

def AnovaOneWayCompareMeans(dfObs, possibleCombs, dfError, MSError, I, useBonferroniCorrection = False):

    if useBonferroniCorrection:
        print 'Bonferroni Correction (alpha\m) @:', str(round(0.05/possibleCombs,6))
        lsdTCrit = GetT_Crit(0.05/possibleCombs,dfError,'two', debug=False)
        print 'T Critical: %s - using %s degrees of freedom (Error df)' %(lsdTCrit, dfError)
    else:
        lsdTCrit = GetT_Crit(0.05,dfError,'two', debug=False)
        print 'T Critical: %s - using %s degrees of freedom (Error df)' %(lsdTCrit, dfError)
     
    print 'MSError: {}, I: {}'.format(str(MSError), str(I))
    lsd = round(lsdTCrit  *  np.sqrt((2 * MSError) / I) , 2)
    print 'LSD :', str(lsd)

    
    print ''
    print'Below, the results are shown in ascending order of magnitude and a line is drawn under pairs of means that do not differ by at least %s, i.e., that are not statistically significantly different.' %lsd
    
    #this is a little of an overkill, but I guess is the simplest way of achiving the result I want
    meansDict = {}
    for col in dfObs.columns:
        meansDict[col] = round (np.mean(dfObs[col]),2)
    meansList = []
    for k,v in sorted(meansDict.items(), key=operator.itemgetter(1)):
       meansList.append ((k,v))    
        
    l1, l2, l3 = '','',''
    for i in range(len(meansList) - 1):      
        labdiff = round(meansList[i+1][1] - meansList[i][1],2)        
        #print meansList[i],  meansList[i+1], labdiff 
        #l1 += str(meansList[i][0]) +'    '
        l1 += '{:5s}'.format(meansList[i][0][:5])   +'    '
        l2 += "%.2f" %  meansList[i][1] +'    ' 
        l3 +=  '|        ' if lsd<labdiff else '|--------'
        
    l1 += str(meansList[i+1][0])
    l2 += "%.2f" %  meansList[i+1][1]
    l3 += '|'    
    print l1,'\n', l2,'\n',l3
