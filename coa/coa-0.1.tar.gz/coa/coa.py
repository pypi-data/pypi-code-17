import sys
import time
import warnings

import numpy as np
from scipy.cluster.vq import kmeans2

warnings.filterwarnings("ignore")
_user_function = None


class Cuckoo:
    def __init__(self, center=None, profit=None, newPos=None):
        self.center = np.random.uniform(COA.varLo, COA.varHi, COA.npar) if center is None else center
        self.numberOfEggs = 0
        self.eggLayingRadiuses = []
        self.newPosition4Egg = newPos if newPos is not None else []
        self.profitValues = profit if profit is not None else 0


class Cluster:
    def __init__(self, positions, profits):
        self.positions = positions
        self.profits = profits
        self.center = []


def time_string(seconds):
    """Returns time in seconds as a string formatted HHHH:MM:SS."""
    s = int(round(seconds))  # round to nearest second
    h, s = divmod(s, 3600)  # get hours and remainder
    m, s = divmod(s, 60)  # split remainder into minutes and seconds
    return '%4i:%02i:%02i' % (h, m, s)


class COA(object):
    npar = 0
    varLo = 0
    varHi = 0

    def cost_function(self, solutions):
        global user_function
        return list(map(_user_function, solutions))

    def __init__(self, cost_function, npar, var_low, var_high, max_iter, radius_coeff=np.random.randint(1,10), motion_coeff=np.random.randint(1,10), number_of_cuckoos=20,
                max_number_of_cuckoos=50, num_of_clusters=1, min_egg_number=2, max_egg_number=4, accuracy=1e-2):

        global _user_function
        COA.npar = npar
        COA.varLo = var_low
        COA.varHi = var_high
        _user_function = cost_function

        self.numOfCuckoos = number_of_cuckoos
        self.maxNumOfCuckoos = max_number_of_cuckoos
        self.maxIter = max_iter
        self.knnClusterNum = num_of_clusters
        self.motionCoeff = motion_coeff
        self.minNumberOfEggs = min_egg_number
        self.maxNumberOfEggs = max_egg_number
        self.radiusCoeff = radius_coeff
        self.accuracy = accuracy
        self.profitVector = []
        self.start = 0

    def run(self):
        self.start = time.time()
        cuckooPop = [Cuckoo() for _ in range(self.numOfCuckoos)]
        globalBestCuckoo = cuckooPop[0].center
        globalMaxProfit = -1 * self.cost_function(np.array([globalBestCuckoo]))[0]
        iteration = 1
        sys.stdout.write('iteration\t\t  profit\t\t\t   elapsed\t\t   remain\n')
        sys.stdout.flush()

        # initialize cuckoos with random values
        while iteration <= self.maxIter and -globalMaxProfit > self.accuracy:

            # evaluate each cuckoo cost
            allPositions = np.array(map(lambda cuckoo: cuckoo.center,cuckooPop))
            tmpProfits = -1 * np.array(self.cost_function(allPositions))
            min_profits, max_profits = np.min(tmpProfits), np.max(tmpProfits)
            coeff = ((self.maxNumberOfEggs - self.minNumberOfEggs) / float(
                max_profits - min_profits)) if max_profits != min_profits else None
            sumOfEggs = 0

            # set each cuckoo egg number due to cost
            for i, cuckoo in enumerate(cuckooPop):
                cuckoo.numberOfEggs = (self.minNumberOfEggs + int(
                    (tmpProfits[i] - min_profits) * coeff)) if coeff else self.maxNumberOfEggs
                sumOfEggs += cuckoo.numberOfEggs

            # set ELR for each cuckoo and egg positions due to ELR
            for cuckoo in cuckooPop:
                eggLayingRadius = float(cuckoo.numberOfEggs) / sumOfEggs * (
                    self.radiusCoeff * (self.varHi - self.varLo))
                cuckoo.eggLayingRadiuses = np.random.uniform(0, eggLayingRadius, cuckoo.numberOfEggs)
                angles = np.linspace(0, 2 * np.pi, cuckoo.numberOfEggs, endpoint=False)
                new_pos = np.array([cuckoo.center + np.array([np.random.choice((-1,1)) *
                                                              cuckoo.eggLayingRadiuses[cnt] * np.cos(angles[cnt]) +
                                                              cuckoo.eggLayingRadiuses[cnt] * np.sin(angles[cnt]) for _
                                                              in range(self.npar)]) for cnt in
                                    range(cuckoo.numberOfEggs)]).clip(self.varLo, self.varHi)
                cuckoo.newPosition4Egg = new_pos[
                    np.append([True], np.any(np.diff(new_pos[np.lexsort(new_pos.T), :], axis=0), 1))].tolist()
                cuckoo.numberOfEggs = len(cuckoo.newPosition4Egg)

            allPositions = np.array(
                [pos for cuckoo in cuckooPop for pos in [cuckoo.center].__add__(cuckoo.newPosition4Egg)])
            tmpProfits = -1 * np.array(self.cost_function(allPositions))

            t = 0
            for cuckoo in cuckooPop:
                cuckoo.profitValues = tmpProfits[t:t + cuckoo.numberOfEggs + 1]
                t += cuckoo.numberOfEggs + 1

            positionAftersort = tmpProfits.argsort()[::-1]
            sortedPositions = allPositions[positionAftersort]
            sortedProfits = tmpProfits[positionAftersort]
            bestCuckooCenter = sortedPositions[0]

            # if numOfCuckoos > maxNumOfCuckoos then get only numOfCuckoos of best cuckoos
            if self.numOfCuckoos > self.maxNumOfCuckoos:
                cuckooPop = [Cuckoo(center=sortedPositions[i], profit=sortedProfits[i], newPos=[sortedPositions[i]]) for
                             i in range(self.maxNumOfCuckoos)]
                self.numOfCuckoos = self.maxNumOfCuckoos
            currentMaxProfit = -1 * self.cost_function(np.array([bestCuckooCenter]))[0]

            if currentMaxProfit > globalMaxProfit:
                globalBestCuckoo, globalMaxProfit = bestCuckooCenter, currentMaxProfit

            self.profitVector.append(-globalMaxProfit)

            # classfing the cuckoos using kmeans into k cluster
            allPositions = np.array([pos for cuckoo in cuckooPop for pos in cuckoo.newPosition4Egg], dtype=np.double)
            clusterNumbers = np.array(kmeans2(allPositions, self.knnClusterNum, minit='points'))
            sidx = clusterNumbers[len(clusterNumbers) - 1].argsort().astype(int)
            split_idx = np.flatnonzero(np.diff(clusterNumbers[len(clusterNumbers) - 1][sidx]) > 0) + 1
            allClusters = np.array(np.split(allPositions[sidx], split_idx))

            clusters = []
            for clstr in allClusters:
                clusters.append(Cluster(clstr, 0))
                clusters[-1].profits = -1 * np.array(self.cost_function(clstr))

            f_mean = [np.mean(clstr.profits) for clstr in clusters]
            indexOfBestCluster = np.argmax(f_mean)
            maxProfitInBestCluster = np.max(clusters[indexOfBestCluster].profits)
            indexOfBestEggPosition = clusters[indexOfBestCluster].profits.tolist().index(maxProfitInBestCluster)

            # find position of best cuckoo in best cluster and migrate all cuckoos to goalpoint
            goalPoint = np.array(clusters[indexOfBestCluster].positions[indexOfBestEggPosition])

            self.numOfCuckoos = 0
            for cluster in clusters:
                cluster.positions = np.array([np.array(position, dtype=np.double) + self.motionCoeff * np.random.ranf(
                    self.npar) * (goalPoint - np.array(position, dtype=np.double)) for position in cluster.positions])
                cluster.positions = np.where(cluster.positions > self.varHi,
                                             cluster.positions - 2 * abs(self.varHi - cluster.positions),
                                             cluster.positions)
                cluster.positions = np.where(cluster.positions < self.varLo,
                                             cluster.positions + 2 * abs(self.varLo - cluster.positions),
                                             cluster.positions)
                cluster.positions = cluster.positions.clip(self.varLo, self.varHi)
                cluster.center = np.mean(cluster.positions, axis=0)
                self.numOfCuckoos += len(cluster.positions)

            cuckooPop = [Cuckoo(center=tmpPos) for cluster in clusters for tmpPos in cluster.positions]
            cuckooPop[-1] = Cuckoo(center=globalBestCuckoo, profit=globalMaxProfit)
            cuckooPop[-2] = Cuckoo(
                center=(np.random.uniform(-1, 1, self.npar) + globalBestCuckoo).clip(self.varLo, self.varHi))
            sys.stdout.write("\r{iter:03d}\t\t{profit:16.11f}\t\t{elapsed}\t\t{remain}".format(iter=iteration,
                           profit=float(-globalMaxProfit),
                           elapsed=time_string(time.time() - self.start),
                           remain=time_string((self.maxIter - iteration) * ((time.time() - self.start) / iteration))))
            sys.stdout.flush()
            iteration += 1

        print('')
        return globalBestCuckoo, -globalMaxProfit
