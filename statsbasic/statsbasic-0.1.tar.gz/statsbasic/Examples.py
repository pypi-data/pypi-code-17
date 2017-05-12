#import statsbasic as sb
#from scipy import stats
#Examples:
#####################################T_test_OneSample

##Exercise 2.1.1 Pag 14
##Head1:
#T_test_OneSample(mu = 21, xbar = 21.06 , S = 0.118, n = 10, alpha = 0.05, tail = 'two')
#
##Head2:
#T_test_OneSample(mu = 21, xbar = 21.33 , S = 0.36, n = 10, alpha = 0.05, tail = 'two')
#
#
##Example 3 Pag 16:
#T_test_OneSample(mu = 90, xbar = 87.9, S = 2.4, n = 5, alpha = 0.05, tail = 'one', direction = 'lower')
#
#
##Homework Questions
##1
#T_test_OneSample(mu = 4, xbar = 5.77, S = 1.572, n = 16, alpha = 0.05, tail = 'two')

#T_test_OneSample(mu = 5, xbar = 6, S = 1, n = 10, alpha = 0.05, tail = 'two')
#
#tt = (xbar - mu)/np.sqrt(S/float(n))  # t-statistic for mean
#pval = stats.t.sf(np.abs(tt), n-1)*2  # two-sided pvalue = Prob(abs(t)>tt)
#print 't-statistic = %6.3f pvalue = %6.4f' % (tt, pval)
#t-statistic =  0.391 pvalue = 0.6955




#
##2
#T_test_OneSample(mu = 12.5, xbar = 12.75, S = 4.3, n = 100, alpha = 0.05, tail = 'one', direction = 'upper')
#
##4
#T_test_OneSample(mu = 72, xbar = 70.4211, S = 9.9480, n = 57, alpha = 0.05, tail = 'two')
#
#
##5
#T_test_OneSample(mu = 3, xbar = 3.8, S = 1.5, n = 15, alpha = 0.05, tail = 'one', direction = 'upper')
#
##6
#T_test_OneSample(mu = 16803, xbar = 15800, S = 2600, n = 30, alpha = 0.05, tail = 'one', direction = 'lower')
#
#
##7
#obs = [2.1, 1.4, 1.3, 1.9, 1.5]
#xbar = np.mean(obs)
#S = np.std(obs, ddof=1) #SAMPLE STANDAR DEVIATION
#T_test_OneSample(mu = 2, xbar = xbar, S = S, n = 5, alpha = 0.1, tail = 'two')
#
#
##8
#T_test_OneSample(mu = 24300, xbar = 26000 , S = 4200, n = 26, alpha = 0.05, tail = 'two')





#####################################T_test_TwoDependentSamples

##Example 4 pag 21
#obs = pd.DataFrame({
#                    'before' : [8085,8544,9002,7786,9498,5906,7078,9766,7109,7802,8213,7184,9824,7136,7216,7708],
#                    'after' : [6644,5818,8942,6939,8594,5488,6124,8137,6907,6154,7709,8235,9711,6514,6907,5413]
#                  })
##The mean of sample differences
#xbar_sample_diffs = round(np.mean(obs.before - obs.after))
#print 'Mean of the differneces:', xbar_sample_diffs
#
##Standard Deviation of sample differences
#S_sample_diffs = round(np.std(obs.before - obs.after, ddof=1))
#print 'sample Standard Deviation of the differneces:', S_sample_diffs 
#T_test_TwoDependentSamples(xbar_sample_diffs = 851, S_sample_diffs = 933, n = 16, alpha = 0.05, tail='two')
###Similar:
#stats.ttest_rel(obs.before, obs.after)

#
##Exercise 2.2.1
#T_test_TwoDependentSamples(xbar_sample_diffs = 10.27, S_sample_diffs = 7.98, n = 11, alpha = 0.05, tail='two')
#
##Example 5 pag 29
#T_test_TwoDependentSamples(xbar_sample_diffs = 1.555, S_sample_diffs = 1.607, n = 40, alpha = 0.05, tail='two')
#
#
##Exercise 2.2.2
#T_test_TwoDependentSamples(xbar_sample_diffs = 0.637, S_sample_diffs = 0.237, n = 6, alpha = 0.05, tail='two')
#
##Exercise 2.2.3
#T_test_TwoDependentSamples(xbar_sample_diffs = 0.55, S_sample_diffs = 0.117, n = 5, alpha = 0.05, tail='two')



#####################################T_test_TwoDependentSamples


##Ex 6 pag43
#sb.T_test_TwoInDependentSamples(xbar_A = 75.509, xbar_B= 78.373, StDev_A= 2.054, StDev_B= 1.635, nA =11, nB =11, alpha = 0.05, tail='two')
#
##2.4.1 pag 48
#T_test_TwoInDependentSamples(xbar_A = 25.32, xbar_B= 31.96, StDev_A= 13.78, StDev_B= 12.05, nA = 25, nB = 25, alpha = 0.05, tail='two')
#
#
##2.4.2 pag 49
#T_test_TwoInDependentSamples(xbar_B = 37.96, xbar_A= 28.66, StDev_B= 11.14, StDev_A= 9.02, nA = 17, nB = 17, alpha = 0.05, tail='two')
#
#
##2.4.5 pag 57
#A = [79.63 ,79.64 ,78.86 ,78.63 ,78.92 ,79.19 ,79.66 ,79.37 ,79.42 ,79.60]
#B = [74.96 ,74.81 ,76.91 ,78.41 ,77.95 ,79.17 ,79.82 ,79.31 ,77.65 ,78.36]
#
#T_test_TwoInDependentSamples(xbar_A = np.mean(A), xbar_B= np.mean(B), StDev_A= np.std(A, ddof=1), StDev_B= np.std(B, ddof=1), nA = 10, nB = 10, alpha = 0.05, tail='two')
#




#####################################CountDataSimpleTest
#Example1
#CountDataSimpleTest(858, 0.53)

#exercise 3.1.1: Referendum poll
#CountDataSimpleTest(1000, 0.35)



#####################################CountData_TwoInDependentSamples

#Example3 - Timolol:
#CountData_TwoInDependentSamples(0.275, 0.129, 0.205, 160, 147, 0.05)


##Exercise 3.2.1
#n1 = 1000
#n2 = 1000
#pYes1 = 0.35
#pYes2 = 0.26
##Question does not give us the pYesTotal, so we have to calculate it
#pYesTotal = ((pYes1 * n1) + (pYes2 * n2)) / (n1 +n2)
#
#CountData_TwoInDependentSamples(pYes1, pYes2, pYesTotal, n1, n2, 0.05)




#Example4 - Cohort Study of Slate Workers:
#CountData_TwoInDependentSamples(0.522, 0.435, 0.48, 726, 529, 0.05)


#Example5 - Oesophageal Cancer Case-Control Study:
#CountData_TwoInDependentSamples(0.48, 0.141, 0.21, 200, 775, 0.05)

#Exercise 3.2.2:
#Exercise 3.2.3:
#Exercise 3.2.4:

#Example6:
    
    
    
#####################################ChiSquare_test

##3.3 Contigency tables (chi square)
##Example 9 - pag 28                
#data = np.array([
#    ['','Timolol','Placebo'],
#    ['Angina Free',44,19],
#    ['Not Angina Free',116,128]
#])
#dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
#ChiSquare_test(dfObs, debug=True)
#
#
##Example 10 - pag 33
#data = np.array([
#    ['','A','B', 'C'],
#    ['Bought',109,49, 168],
#    ['Heard-no-buy',55,56, 78],
#    ['Never heard ',36,45, 54]
#])
#dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0], columns=data[0,1:]).apply(pd.to_numeric,axis=0)
#sb.ChiSquare_test(dfObs, debug=True)
##
#
##Example 11: Literary Style - pag 40
#data = np.array([
#    ['','Sensibility','Emma', 'Sanditon-A' , 'Sanditon-B'],
#    ['a',147, 186, 101, 83],
#    ['an', 25, 26 ,11 ,29],
#    ['this', 32, 39, 15, 15],
#    ['that', 94, 105, 37, 22],
#    ['with', 59, 74, 28, 43],
#    ['without', 18, 10, 10, 4]
#])
#dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0], columns=data[0,1:]).apply(pd.to_numeric,axis=0)
##Check her own work (Ignore B 'Sanditon-B' is the imitator)
#ChiSquare_test(dfObs[['Sensibility','Emma', 'Sanditon-A' ]], debug=True)
#
#
##Check her own work (Ignore B 'Sanditon-B' is the imitator)
#dfObs['Austen'] = dfObs['Sensibility'] + dfObs['Emma'] + dfObs['Sanditon-A' ]
#ChiSquare_test(dfObs[['Austen', 'Sanditon-B' ]], debug=True)
                  



#https://classroom.udacity.com/courses/ud201/lessons/1331738563/concepts/1895400350923            
#data = np.array([
#    ['','Successful','unsuccessful'],
#    ['Ex Freq',33,67],
#    ['Obs Freq',41,59]
#])
#dfObs = pd.DataFrame(data=data[1:,1:], index=data[1:,0],    columns=data[0,1:]).apply(pd.to_numeric,axis=0)
#ChiSquare_test(dfObs, debug=True)




#Example 12: Mendels Pea Plant Data
#Exercise 3.3.3

#Exercise 3.3.4

#Exercise 3.3.5

#Example 13: Random Number Generation

#Example 14: Lotto Numbers


#################ANOVA

##Example 1: Laboratory Comparisson Study - pag1
#labels = ['lab1', 'lab2', 'lab3', 'lab4']
#data =[[4.9, 5.7, 5.1, 5.3, 5.4, 5.5],
#       [5.4, 5.5, 4.8, 4.9, 5.2, 5.4],
#       [5.8, 6.0, 6.0, 5.5, 5.9, 5.8],
#       [4.5, 4.9, 4.7, 4.7, 4.4, 4.8]]
#
#dfObs = sb.CreateAnovaDataFrame(labels, data)
#sb.AnovaOneWay(dfObs)
#
##SAME TEST FROM SCIPY
#from scipy import stats
#stats.f_oneway(data[0],data[1],data[2],data[3])


#
#
##Exercise 5.1.1 Iris - pag 17
#import statsbasic as sb
#labels = ['Brown', 'Green', 'Blue']
#data =[[26.8, 26.9, 23.7, 25.0, 26.3, 24.8],
#       [26.4, 24.2, 28.0, 26.9, 29.1, 26.9],       
#       [26.7, 27.2, 29.9, 28.5, 29.4, 28.3]]
#
#dfObs = sb.CreateAnovaDataFrame(labels, data)
#sb.AnovaOneWay(dfObs)
#
#
#
##Example 2 - pag 18
#labels = ['1', '2', '3','4', '5', '6']
#data =[[73,102,118,104,81,107,100,87,117,111],
#       [98,74, 56, 111,95, 88, 82,77, 86, 92], 
#       [94, 79, 96, 98, 102,102,108,91, 120,105],
#       [90,76,90,64,86,51,72,90,95,78],
#       [107,95, 97, 80, 98, 74, 74, 67, 89,58],
#       [49,82,73,86,81,97,106,70,61,82]]
#
#dfObs = CreateAnovaDataFrame(labels, data)
#AnovaOneWay(dfObs)



#regression silly test:
#df = pd.read_csv('C:\\git\\PostGradStats\\M2\\trees.csv')
#
#plt.scatter(df.Diam,df.Volume)
#plt.xlabel('Diameter')
#plt.ylabel('Volume')
#
#
#
#num_points = 10
#np.mean(df.Diam) #13.248
#
#labels = []
#data = []
#for index, row in df.iterrows():
#    name = 'Obs_{}'.format(index+1)
#    labels.append(name)
#    
#    v = []
#    for i in xrange(num_points):
#        y1 = np.random.normal(row['Diam'],1)
#        v.append(y1)
#    data.append(v)
#
#dfObs = CreateAnovaDataFrame(labels, data)
#print tabulate(dfObs[['Obs_4', 'Obs_5','Obs_6','Obs_7', 'Obs_8', 'Obs_9', 'Obs_10', 'Obs_11', 'Obs_12', 'Obs_13', 'Obs_14']], headers='keys', tablefmt='psql') 
#AnovaOneWay(dfObs[['Obs_4', 'Obs_5','Obs_6','Obs_7', 'Obs_8', 'Obs_9', 'Obs_10', 'Obs_11', 'Obs_12', 'Obs_13', 'Obs_14']])
#
#
#np.min(df.Volume), np.max(df.Volume) # 10 - 70



