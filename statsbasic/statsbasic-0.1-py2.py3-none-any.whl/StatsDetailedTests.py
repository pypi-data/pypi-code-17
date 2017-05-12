#%load_ext autoreload
#%autoreload 2
from tabulate import tabulate  #pretty print
from scipy.stats import chi2
from scipy import stats
import pandas as pd
import numpy as np
import math 
from matplotlib import pyplot as plt
import StatsDetailedTestsHelper as StatsHelper

#How to make IPython notebook matplotlib plot inline:
#http://stackoverflow.com/questions/19410042/how-to-make-ipython-notebook-matplotlib-plot-inline/27436973
def T_test_OneSample(mu, xbar, S, n, alpha, tail = 'two', direction = 'none'):
    #1) Get Standard error of xbar  
    SE_xbar = S / math.sqrt(n)
    print 'SE(xbar):', round(SE_xbar,3)
    
    #2) Get the t-statistic
    t_stat = (xbar - mu) / SE_xbar
    print 't statistic:', round(t_stat,3)
    
    #3) Get t-critical:
    auxlabel =''
    if tail =='two':
        alpha = alpha /2
        auxlabel = '+-'
    elif tail == 'one':
        #just keeing this here to remmebr that the stats.t.ppf assumes one-tail 
        alpha = alpha # :)  no need to change alpha; 
          
    t_crit = stats.t.ppf(1-alpha, n-1)   
    if tail == 'one' and direction == 'lower':
        t_crit = t_crit * -1 # gets the negative end of the t-crit distribution
    print 't crit:', auxlabel +str(round(t_crit,2))
    
    StatsHelper.InterpretT_Stat(t_crit,t_stat, tail, direction)
    
    StatsHelper.CalculateCI(t_crit, xbar, SE_xbar)


##################################################PAIRED COMPARISONS
#2.2) Two Samples - Paired (dependent Samples)
#Two measurements on the same participant (Before \ After)
def T_test_TwoDependentSamples(xbar_sample_diffs, S_sample_diffs, n , alpha, tail = 'two', direction = 'none'):
    print 'Two Dependent Sample t-test'    
    print 'Ho: muA - muB = 0 (Is the mean of the differences equal to zero?)\n'
    
    #1) Get Standard error of xbar  
    SE_xbar = S_sample_diffs / math.sqrt(n)
    print 'SE(d_bar):', round(SE_xbar,3)
    
    #2) Get the t-statistic
    pop_mean = 0 # that's the null Hypotheys
    t_stat = (xbar_sample_diffs - pop_mean) / SE_xbar
    print 't statistic:', round(t_stat,3)
    
    #3) Get t-critical:
    df = n-1
    t_crit = StatsHelper.GetT_Crit(alpha, df, tail)
    
    StatsHelper.InterpretT_Stat(t_crit, t_stat, tail)
    
    StatsHelper.CalculateCI(t_crit, x_bar = xbar_sample_diffs, SE_xbar = SE_xbar)
    

#2.3) Two Samples - Between samples (Independent Samples)
#Two measurements - different participants 
def T_test_TwoInDependentSamples(xbar_A, xbar_B, StDev_A, StDev_B, nA, nB, alpha, tail = 'two', direction = 'none'):
    print 'Two Independent Sample t-test'
    print 'Ho: muA - muB = 0 (Do both samples come from the same population?)\n'
    
#    avg_variances = ((StDev_A ** 2) + (StDev_B ** 2) ) / 2
#    print 'Average of both Sample Variations:', round(avg_variances,3)
#    SE = math.sqrt ((2 * avg_variances)/n)
#    print 'SE of the difference between two independent sample means:', round(SE,3)    
    
    avg_variances = ((StDev_A ** 2)/nA)  + ((StDev_B ** 2)/nB)
    SE = math.sqrt (avg_variances)
    print 'SE of the difference between two independent sample means:', round(SE,3)
    
    #we are testing if the difference of the population means is zero (thats Ho)
    #in other words, if the mu of both populations is the same
    dif_pop_mean = 0
    t_stat = (((xbar_B - xbar_A) - dif_pop_mean)) / SE
    print 't statistic:', round(t_stat,3)
    
    df = (nA-1) +  (nB-1)
    t_crit = StatsHelper.GetT_Crit(alpha, df, tail)    
    StatsHelper.InterpretT_Stat(t_crit, t_stat, tail)
    StatsHelper.CalculateCI(t_crit, x_bar = (xbar_B - xbar_A), SE_xbar = SE )
    
    print ''
    print 'Testing if Standar Deviations are the same: Ho: StDev_A / StDev_B == 1'
    f_ratio = round( (max(StDev_A, StDev_B) / min(StDev_A, StDev_B)) ** 2 ,3)
    print 'f ratio:', round(f_ratio,3)

    f_crit = StatsHelper.GetF_Crit(alpha, nA-1, nB-1, tail)    
    
    if tail =='two':        
        if f_ratio < f_crit * -1 or f_ratio > f_crit:
            print 'Reject Ho - Standard Deviations are not the same'
        else:
            print 'There is no reason to reject the assumption of equal underlying standard deviations'
    print ''
    r2 = round((t_stat ** 2) / (t_stat**2 + df),4)
    print 'Proportion of the difference between means that can be explained (r^2):{}'.format(r2)
    
    




##########Chapter3
#n = Samples Size
#p = percentage of the sample who said Yes
def CountDataSimpleTest (n, p, alpha=0.05):
#    n = 1000
#    p = 0.35
#    alpha = 0.05
  
    #Standar Error of p
    SEp = np.sqrt( (p * (1-p))/n  )
    
    #Divide alpha by 2 because we want two tail test
    alpha = alpha/2
    #Note that for count data the relevant reference distribution for calculating 
    #confidence intervals is the standard Normal (never the t-distribution). 
    Zvalue = round(stats.norm.ppf(alpha) * -1,2)
    
    CI =  round(Zvalue * SEp,3)
    lCI = round(p - CI, 4)
    uCI = round(p + CI, 4)
    
    print 'A %s CI for the population proportion who said yes is given by:' %"{0:.0f}%".format((1-alpha*2) * 100) 
    print lCI, uCI
    print 'We estimate that between %s and %s of the population of voters intended to say yes' %("{0:.0f}%".format(lCI*100) , "{0:.0f}%".format(uCI*100) )


#3.2 Simple Comparative Studies  - INDEPENDENT TESTS
#The statistical problem is to assess the extent to which observed sample differences are likely to be systematic 
#and not simply due to chance variation.

#The statistical questions that we typically wish to address are whether or not the population or 
#process proportions are the same and, if there is a difference, how big is that difference?

def CountData_TwoInDependentSamples(pYes1, pYes2, pYesTotal, n1, n2, alpha):
#    pYes1 = 0.275 #patients that "got cured" by using the medicine
#    pYes2 = 0.129 #patients that "got cured" by the placebo
#    pYesTotal = 0.205 #total patients that "got cured" 
#    
#    n1 = 160
#    n2 = 147
#    alpha=0.05
    
    alpha = alpha/2 # always two tail test
    print 'CountData: Two InDependent Proportions Test'
    print 'Ho: pi1 - pi2 = 0 (Same population proportions)'
    print ''
    
    SE_diff = np.sqrt(
                   ((pYes1 * (1-pYes1))/n1) + 
                   ((pYes2 * (1-pYes2))/n2) 
                 )   
    print 'Standar Error of the differneces:', round(SE_diff,4)    
    ZCrit = round(stats.norm.ppf(alpha) * -1, 2)
    print 'z crit: +-'+str(ZCrit)

    lCI, uCI = StatsHelper.CalculateCI(ZCrit, x_bar = (pYes1 - pYes2), SE_xbar = SE_diff)
    
    
    #Using a "medicine example"
    print """The interval suggests that the difference between population proportions is between %s and %s 
              """ %("{0:.0f}%".format(lCI*100) , "{0:.0f}%".format(uCI*100) )
    
    if lCI >0:
        print 'Interval does not contain 0, therefore there was a significant impact'
    else:
        print 'Interval contains 0, therefore there was not a significant impact'
    
    print ''
    
    #Because pi (pop proportion) is unknown it must be estimated from the sample data.  
    #If there is no group difference (Ho) then a natural estimator is the overall sample proportion of patients who become cured 
    estimatedSE = np.sqrt(
                   ((pYesTotal * (1-pYesTotal))/n1) + 
                   ((pYesTotal * (1-pYesTotal))/n2) 
                 )
    dif_pop_mean = 0
    z_stat = (((pYes1 - pYes2) - dif_pop_mean)) / estimatedSE
    print 'z statistic:', round(z_stat,3), ' - this is using the estimated population proportion of', pYesTotal, 'therefore a SE of', round(estimatedSE,4)
    
    #Its called T, but the logic is the same, so I can use it:
    StatsHelper.InterpretT_Stat(ZCrit, z_stat, "two")
    
    print ''
    print 'OBS: The Z value has a standard Normal distribution; when the standard Normal is squared it gives a chi-square distribution with one degree of freedom, which is the sampling distribution of the X2 statistic.'
    print 'The Z-test for the difference between the population proportions gives a test statistic of Z=', str(round(z_stat,3)),'- when this is squared it gives:', str(round(z_stat**2,3)), 'which is the same as the X2 statistic you would get if run a chi-square test (apart from the effects of rounding).'
    print 'Also, the square of the critical values for the standard Normal distribution equals the critical value for the chi-square test (1.96=3.84) the two tests are, therefore, equivalent.'
    print ''
    
    nYes1 = round(n1 * pYes1,0)
    nNo1  = n1 - nYes1

    nYes2 = round(n2 * pYes2,0)
    nNo2  = n2 - nYes2
    
    print 'Odds ratio:', round((nYes1 / nNo1) / (nYes2/nNo2),1)
    #print 'OBS2: Given that this test only accepts probabilities as


def ChiSquare_test(df, debug=False):
    dfObs = df.copy() # avoids messing with the original data frame
    
    print 'Ho: There is a set of population relative frequencies for these groups\n'

    if debug:
        print 'Observed values:'
        print tabulate(dfObs, headers='keys', tablefmt='psql') 
    #1)Calculate Expected Table
    #Smart way to multiply the cell's row total by the cell's column total and divide by the total N
    dfExpected = dfObs.apply(lambda r: dfObs.sum()[r.name]*dfObs.sum(1)[r.index]/dfObs.sum().sum())
    dfExpected = dfExpected.round(2)
    if debug:
        print 'Expected:'    
        print tabulate(dfExpected, headers='keys', tablefmt='psql') 
    
    
    #not being smart this time:
    #This is a silly but intuitive way of measuring the difference from the Expected table: 
    #((O - E)^2) /E
    for i in range(len(dfObs)):
        for j in range(len(dfObs.columns)):
            dfObs.iloc[i,j] = round( ( (dfObs.iloc[i, j]  - dfExpected.iloc[i,j]) ** 2) / dfExpected.iloc[i,j] ,2)

    if debug:
        print '(Divergences between the observed and expected values) ^2  divided by the Expected value:'
        print tabulate(dfObs, headers='keys', tablefmt='psql')             
    
    
    chi_stat = round(dfObs.sum().sum(),2)
    print 'Chi_sq:', chi_stat
    df = (len(dfObs) -1) * (len(dfObs.columns) - 1)
    
    chi_crit = chi2.isf(q=0.05, df=df)
    print 'Chi_crit:', chi_crit, '('+str(df)+' degree(s) of freedom)'
    
    #This should be improved:
    if  chi_stat > chi_crit:
        print 'Reject the null hypothesis;\nThe test result suggests a systematic difference between the observed and expected values. This points to a difference between the groups in terms of the long-run proportions.'
    else:
        print 'Cannot Reject Ho'


#################Chapter 4 ANOVA
#https://onlinecourses.science.psu.edu/stat414/node/218

def CreateAnovaDataFrame(labels, data):        
    dfObs = pd.DataFrame()
    i=0
    for d in data:
        dfObs[labels[i]] = d
        i+=1
    return dfObs
    
def AnovaOneWay(dfObs):   
    print 'Anova Test: Is there a statistical difference between the mean of the populations?'
    
    I = len(dfObs)
    J = len(dfObs.columns)
    print 'Number of Rows:', I
    print 'Number of Columns:', J
    
    #number of possible 2 by 2 combinations
    possibleCombs = (J * (J-1)) /2
    
    #average acroos the whole dataset 
    x_doublebar = np.average(dfObs)
    
    #Sum of Squares Between Groups (Model) ((Xij - x_doublebar)**2)/I
    SSM = 0
    
    #Sum of Squares WithIn each Group (Error)  (Xij - Xbarj) **2
    SSE = 0
    
    for col in dfObs.columns:
        x_bar = round(np.mean(dfObs[col]),6)    
        #WithIn Group Variation:
        SSE += np.sum( (dfObs[col] - x_bar) **2)
    
        #BetweenGroup Variation - I think this definition is inccomplete in the notes;
        #So I looked at what the stats.f_oneway does an it is something like this:
            
        #For each element of the column, get the difference from the overall mean
        #sum the differences and square the sum
        #then divide by the number of elements
        #SSM += (np.sum( dfObs[col] - x_doublebar) ** 2) / I
        
        #Option2: Alternatively (which matches the notes - except for the last step), 
        #we can square the diference 
        #between the group mean and the overall mean and multiply by I
        SSM +=  ((x_doublebar - x_bar) **2 ) * I
    
    dfModel = J - 1      #DF between Groups    
    dfError  = J * (I-1) #DF WithInGroups
    df = dfModel  +     dfError
      
    #asserting that df total = (nrows * ncolumns) -1
    assert (I * J) -1 == df
    
    SSM = round(SSM,6)
    SSE = round(SSE,6)
    
    MSModel = round(SSM/dfModel ,6)
    MSError = round(SSE/dfError,6)
    FValue = round(MSModel / MSError,6)
        
    AnovaData = np.array([
        ['Source','SumSquares','DF'     , 'MeanSquare', 'F-Value'],
        ['Model' , SSM        , dfModel , MSModel     , FValue ],
        ['Error' , SSE        , dfError , MSError     , ''],
        ['Toltal', SSM + SSE  , df      , ''         , '']
    ])
    dfAnova = pd.DataFrame(data=AnovaData[1:,1:], index=AnovaData[1:,0], columns=AnovaData[0,1:])
    print tabulate(dfAnova , headers='keys', tablefmt='psql')    
    print 'Mean Square Error(%s) is equal to the average of the within-group variances' %(MSError)
    assert MSError == round(sum(np.std(dfObs, ddof=1)**2)/len(dfObs.columns),6)

    FCrit = StatsHelper.GetF_Crit(0.05, dfModel, dfError, 'one')
    
    StatsHelper.plotFDistribution(FCrit, FValue, dfModel, dfError)
    
    if FValue < FCrit :
        print 'Cannot Reject Ho'
        return
    else:
        print 'Reject Ho: The F-test has established that not all the means are the same'
    
    print 'Continuing Analysis....'        
    #If cannot reject Ho, continue analysis    
    
    
    #Residual Plot
    for col in dfObs.columns:
        #Its not really a scatter plot but it is simple and prouduces a good result :)
        plt.scatter([np.average(dfObs[col], axis=0) for j in range(len(dfObs))], dfObs[col] - np.mean(dfObs[col]))        
    plt.axhline(y=0,xmin=0,xmax=3,c="blue",linewidth=0.5,zorder=0)
    plt.xlabel('Fitted Values (Y bar)')
    plt.ylabel('Residuals')
    plt.title("Residuals versus fitted values (group means)")
    
    plt.legend(loc="upper left", bbox_to_anchor=(1,1))  
    plt.show()
    
    #Comparing Means - Least Significant Difference
    print 'Least Significant Difference Analysis - Smallest difference between two sample means that will be declared statistically significant'
    StatsHelper.AnovaOneWayCompareMeans(dfObs, possibleCombs, dfError, MSError, I, useBonferroniCorrection = False)
    #Using Bonferroni Correction
    print''
    print''
    print''
    StatsHelper.AnovaOneWayCompareMeans(dfObs, possibleCombs, dfError, MSError, I, useBonferroniCorrection = True)