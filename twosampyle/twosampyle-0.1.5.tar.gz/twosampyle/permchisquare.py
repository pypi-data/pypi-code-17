def chi_squared_statistic(o,e):
    """"""
    
    o = np.array(o)
    e = np.array(e)
    return np.sum(1.0*(o - e)**2 / e)


class ChiSquaredTest():
    
    def __init__(self, observed=None, expected=None):
        self.observed = observed
        self.expected = expected
        
        
    def plot_dsn(self, k=100):
        simulated_stats = self.simPermDsn(k=k)
        tit = "Chi-Squared Test Statistic Distribution for k={} Simulations".format(k)
        plot_hist(simulated_stats, title=tit, xlabel="Test Statistic Value", ylabel="Frequency")
    
    
    def testStat(self, input_observed=None, input_expected=None):
        if input_observed or input_expected:
            chisq_teststat = chi_squared_statistic(input_observed, input_expected)
        else:
            chisq_teststat = chi_squared_statistic(self.observed, self.expected)
        return chisq_teststat
    
    def simPermDsn(self, input_observed=None, input_expected=None, k=100):
        if input_observed or input_expected:
            test_stat = self.testStat(input_observed, input_expected)
            n = len(input_observed)
        else:
            test_stat = self.testStat()
            n = len(self.observed)
            
        # create sampling distribution
        chisqrd_vals = []
        for i in range(k):
            values = np.random.random((n,))
            ex = 1.0*n/2
            values[values<.5]=0
            values[values>=.5]=1
            diff1 = chi_squared_statistic(sum(values==0),ex)
            diff2 = chi_squared_statistic(sum(values==1),ex)
            chisqrd_vals.append(diff1+diff2)
        return chisqrd_vals
    
    def pvalue(self, input_observed=None, input_expected=None):
        
        current_stat = self.testStat(input_observed, input_expected)
        simulated_stats = self.simPermDsn(input_observed, input_expected)
        
        # p-value = proportion of test stats greater than ours
        p_value = 1.0*sum(simulated_stats >= current_stat) / len(simulated_stats)
        return p_value
