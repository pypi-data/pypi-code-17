
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from twosampyle.plot_utils import plot_hist

class PermTest(object):
    
    
    def __init__(self, data):
        """"""
        self.data = data
        self.formatted_data = None
        
        
        
    def format_data(self, response1=None, response2=None):
        """
        Converts data from a 2-column format (where each column refers to a treatment type) to
        a 2-column format where response is one column, treatment is the other.

        This is done for both efficiency of storage and test runtime.

        :param data: pandas DataFrame. each column must be of same length
        :return: pandas DataFrame in response, treatment format
        """
        # create new treatment Series
        
        if (response1==None) and (response2==None):
            # No columns specified, so default to first 2
            
            nrow, ncol = self.data.iloc[:,[0,1]].shape
            treatment_column = pd.Series([self.data.iloc[:,[0,1]].columns.values[i]
                            for i in range(ncol)
                            for j in range(nrow)], dtype='category')
            response_column = pd.concat([self.data.iloc[:,0],
                                         self.data.iloc[:,1]]).tolist()
        else:
            
            nrow, ncol = self.data.loc[:,[response1,response2]].shape
            treatment_column = pd.Series([self.data.loc[:,[response1,response2]].columns.values[i]
                            for i in range(ncol)
                            for j in range(nrow)], dtype='category')
            response_column = pd.concat([self.data.loc[:,response1],
                                         self.data.loc[:,response2]]).tolist()

        self.formatted_data = pd.DataFrame({"response": response_column,
                                      "treatment": treatment_column})

        
                
            
    def diff_means(self, response="response", treatment="treatment", data=None):
        """Calculates the difference of means between the two treatment groups"""
        if data is None:
            trt1 = self.formatted_data[treatment].cat.categories[0]
            trt2 = self.formatted_data[treatment].cat.categories[1]

            mean_diff = self.formatted_data[response][self.formatted_data[treatment]==trt1].mean() \
            - self.formatted_data[response][self.formatted_data[treatment]==trt2].mean()

            return mean_diff
        else:
            trt1 = data[treatment].cat.categories[0]
            trt2 = data[treatment].cat.categories[1]

            mean_diff = data[response][data[treatment]==trt1].mean() \
            - data[response][data[treatment]==trt2].mean()

            return mean_diff
    
    
    def simPermDsn(self, response="response", treatment="treatment", test="mean", k=100):
        """
        Creates permutation distributionn consisting of k values for our data
        :param response: column of response values
        :param treatment: column of treatment levels
        :param test: string detailing test to use. 
        :param k: integer specifying number of values in permuted distribution
        :return:
        """
        df = self.formatted_data[:]
        testStatistics = []
        if test == "mean":
            for simulation in range(k):
                df[treatment] = pd.Series(np.random.permutation(self.formatted_data[treatment]),
                                            dtype='category')
                testStatistics.append(self.diff_means(response=response, treatment=treatment, data=df))

            return testStatistics
        
    def pvalue(self, response="response", treatment="treatment", test="mean", k=100):
        """Returns p-value for our test"""
        if test == "mean":
            current_stat = self.diff_means(response=response, treatment=treatment)

            simulated_stats = self.simPermDsn(response=response, treatment=treatment, test=test, k=k)
            simulated_stats = np.array(simulated_stats)
            p_value = 1.0 * sum(abs(simulated_stats) >= abs(current_stat))/k

            return p_value
        
    def plot_dsn(self, response="response", treatment="treatment", test="mean", k=100):
        """Plots distribution of test statistics"""
        simulated_stats = self.simPermDsn(response=response, treatment=treatment, test=test, k=k)
        test_statistic = self.diff_means(response, treatment)
        tit = "Permutated Test Statistic Distribution for k={} Simulations".format(k)
        plot_hist(simulated_stats, title=tit, xlabel="Test Statistic Value", ylabel="Frequency", test_stat=test_statistic)

