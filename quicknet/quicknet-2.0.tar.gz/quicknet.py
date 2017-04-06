import numpy as np
import random
import math

def nonlin(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)

	return 1/(1+np.exp(-x))

def inverseNonlin(x):
        return np.log(x/(1-x))

def getChanges(layers, weights, error, learningRate):
        latestDelta = error*nonlin(layers[-1], deriv = True)
        changes = []
        changes.append(latestDelta.dot(layers[-2].T)*learningRate)
        for i in range(1, len(layers)-1):
            layer = layers[-i-1]
            latestDelta = (weights[-i].T.dot(latestDelta))*nonlin(layer, True)
            changes.append(latestDelta.dot(layers[-i-2].T)*learningRate)
        return changes

def getLayers(inputs, weights, dropout = False):
        result = []
        result.append(inputs)
        for i in range(len(weights)):
            layer = nonlin(weights[i].dot(result[-1]))
            if not(i == len(weights)-1) and dropout:
                    dropOut(layer, 0.8)
            result.append(layer)
        return result

def dropOut(layer, probability):
        for i in range(len(layer)):
            for j in range(len(layer[0])):
                if random.random() > probability:
                        layer[i][j] = 0

def applyChanges(matrix, changes):
        for i in range(len(changes)):
            matrix[-i-1] += changes[i]

def train(weights, steps, batchSize, inputs, outputs, learningRate):
        layers = []
        j = 0
        k = 0
        while j < len(outputs[0]):
            if j + batchSize > len(outputs[0]):
                k = len(outputs[0]) - j
            else:
                k = j + batchSize
            for i in range(steps):
                layers = getLayers(inputs[:, j:k], weights)
                error = (outputs[:, j:k]/layers[-1] - (1-outputs[:, j:k])/(1-layers[-1]))
                changes = getChanges(layers, weights, error, learningRate/(k-j))
                applyChanges(weights, changes)
                
            j += batchSize


def run(weights, inputs, outputs):
        layers = getLayers(inputs, weights)
        return layers[-1]

def countMistakes(errors):
        mistakes = 0
        for e in errors[0]:
                if e > 0.4:
                        mistakes += 1
        return mistakes
