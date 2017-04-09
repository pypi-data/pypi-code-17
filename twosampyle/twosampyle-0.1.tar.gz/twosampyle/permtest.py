class PermTest(object):
    
    def __init__(self, data):
        self.data = data
        self.formatted_data = None

    def format_data_from_two_response(self, response1, response2):
        """
        Converts data from a 2-column format (where each column refers to a treatment type) to
        a 2-column format where response is one column, treatment is the other.

        This is done for both efficiency of storage and test runtime.

        :param data: pandas DataFrame. each column must be of same length
        :return: pandas DataFrame in response, treatment format
        """
        # create new treatment Series
        nrow, ncol = self.data.shape
        treatment_column = pd.Series([self.data.columns.values[i]
                                      for i in range(ncol)
                                      for j in range(nrow)], dtype='category')

        # create response vector
        if type(response1) == str and type(response2) == str:
            response_column = pd.concat([self.data.loc[:, response1],
                                         self.data.loc[:, response2]]).tolist()
        else:
            raise ValueError("response inputs must correspond to either column number(int) or name(str)")

        self.formatted_data = pd.DataFrame({"response": response_column,
                                            "treatment": treatment_column})

    def diff_means(self, response="response", treatment="treatment", data=None):
        """"""
        if data is None:
            trt1 = self.formatted_data[treatment].cat.categories[0]
            trt2 = self.formatted_data[treatment].cat.categories[1]

            mean_diff = self.formatted_data[response][self.formatted_data[treatment] == trt1].mean() \
                        - self.formatted_data[response][self.formatted_data[treatment] == trt2].mean()

            return mean_diff
        else:
            trt1 = data[treatment].cat.categories[0]
            trt2 = data[treatment].cat.categories[1]

            mean_diff = data[response][data[treatment] == trt1].mean() \
                        - data[response][data[treatment] == trt2].mean()

            return mean_diff

    def simPermDsn(self, response="response", treatment="treatment", test="mean", k=100):
        """
        Creates permutation dsn for our data
        :param data:
        :param hasTrt:
        :param testStat:
        :param k:
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

    def test(self, response="response", treatment="treatment", test="mean", k=100):
        """"""
        if test == "mean":
            current_stat = self.diff_means(response=response, treatment=treatment)

            simulated_stats = self.simPermDsn(response=response, treatment=treatment, test=test, k=k)
            simulated_stats = np.array(simulated_stats)
            p_value = 1.0 * sum(abs(simulated_stats) >= abs(current_stat)) / k

            return p_value

    def plot_dsn(self, response="response", treatment="treatment", test="mean", k=100):
        """"""
        simulated_stats = self.simPermDsn(response=response, treatment=treatment, test=test, k=k)
        tit = "Permutation Test Statistic Distribution for k={} Simulations".format(k)
        plot_hist(simulated_stats, title=tit, xlabel="Test Statistic Value", ylabel="Frequency")
