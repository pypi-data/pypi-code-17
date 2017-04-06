#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__      = 'Tao Peter Wang'
__version__     = '0.1.5'
__license__     = 'MIT'
__email__       = 'peterwangtao0@hotmail.com'
__date__        = 'Dec-14-2016'

import sys
import numpy as np

class Voter(object):
    'Probablistic Majority Voting class'

    def __init__(self, probabilities, categories):
        self.probabilities = probabilities
        self.categories = categories
        try:
            self.check_arguments()
            self.probabilities = self.probabilities.tolist()
        except Exception:
            raise               # in which case the object creation (__new__()) will fail

    def vote(self, windows=5):
        if windows <= 1 or windows % 2 == 0:
            raise ValueError('Number of windows has to be a positive odd number larger than 1')

        results_index = []
        results_names = []

        # first couple windows, go with popular votes
        for w in range(0, (windows - 1) // 2):
            cut = self.probabilities[:w + (windows - 1) // 2 + 1]
            maxindex = self.__get_popular(cut, len(self.categories))
            results_index.append(maxindex)
            results_names.append(self.categories[maxindex])

        # middle part
        for w in range((windows - 1) // 2, len(self.probabilities) - (windows - 1) // 2):           # window for which to calculate the voting results
            cut = self.probabilities[w - (windows - 1) // 2 : w + (windows - 1) // 2 + 1]           # all voters
            maxindex = self.__get_majority(cut, windows, len(self.categories))
            results_index.append(maxindex)
            results_names.append(self.categories[maxindex])

        # last couple windows, go with popular votes
        for w in range(len(self.probabilities) - (windows - 1) // 2, len(self.probabilities)):
            cut = self.probabilities[w - (windows - 1) // 2:]
            maxindex = self.__get_popular(cut, len(self.categories))
            results_index.append(maxindex)
            results_names.append(self.categories[maxindex])

        return results_index, results_names

    def __get_majority(self, cut, windows, cats):
        single_window = [[] for i in range(cats)]

        for voter in cut:
            cur_max = -sys.maxsize - 1
            for i in range(cats):
                if voter[i] > cur_max:
                    cur_max = voter[i]
            single_window[voter.index(cur_max)].append(voter)       # append to respective windows
        
        # the new way
        len_list = [[] for i in range(cats)]                        # number of voters for each category
        for i in range(cats):
            len_list[i] = len(single_window[i])
        
        maxlen = -sys.maxsize - 1
        for l in len_list:                                          # find the amx
            maxlen = max(maxlen, l)
        
        nummax = 0
        for l in len_list:                                          # check singularity of max
            nummax = nummax + 1 if l == maxlen else nummax
        if nummax > 1:                                             # tied
            maxindices = []
            for i in range(len(len_list)):                          # obtain all tied contenders
                if len_list[i] == maxlen:
                    maxindices.append(i)

            maxprobs = [0 for _ in range(cats)] 
            for win in cut:
                for ind in maxindices:
                    maxprobs[ind] += win[ind]
            maxindex = 0
            maxprob = 0
            for ind in maxindices:
                if maxprobs[ind] > maxprob:
                    maxprob = maxprobs[ind]
                    maxindex = ind
            return maxindex

        # the old way
        # len_list = sorted(len_list, reverse=True)                   # descending order

        # if len_list[0] == len_list[1]:                              # more than one majority
        #     # when electoral collage fails, we count on popular votes
        #     return self.__get_popular(cut, cats)
        else:                                                        # clear winner
            maxlen = 0
            maxindex = 0
            for i in range(len(single_window)):
                if len(single_window[i]) > maxlen:
                    maxlen = len(single_window[i])
                    maxindex = i
            return maxindex

    def __get_popular(self, cut, cats):
        popvotes = [0] * cats
        for voter in cut:
            for i in range(cats):
                popvotes[i] += voter[i]
        maxvotes = 0
        maxindex = 0
        for i in range(cats):
            if popvotes[i] > maxvotes:
                maxvotes = popvotes[i]
                maxindex = i
        return maxindex

    def check_arguments(self):
        if type(self.probabilities) is not np.ndarray or type(self.categories) is not list:
            raise TypeError('Input argument type incorrect')
        elif len(self.probabilities) <= 0:
            raise Exception('No windows with predicted probabilities found in the table')
        elif len(self.probabilities[0]) != len(self.categories):
            raise IndexError('Number of categories does not match the columns in the table')

def main():
    print("Only meant to be called from other program through imports")

if __name__ == "__main__":
    main()