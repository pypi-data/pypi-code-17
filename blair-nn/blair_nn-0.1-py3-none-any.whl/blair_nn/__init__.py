import numpy as np
import matplotlib.pyplot as plt


class NN:
    """
    Provides methods for training and predicting with a feed forward neural network and evaluating performance of that
    network.
    """
    def __init__(self):
        self.epochs = None
        self.weights = None
        self.mse = None
        self.mse_log = []
        self.y_pred = None
        self.activation_fun = None

    def fit(self, X, y, nh_units, activation_fun, max_epochs=1000, mse_threshold=.1, lr=.1):
        """
        Fits and trains a feed forward neural network using vanilla backpropogation.
        Args:
            X: numpy array of features
            y: numpy array of response (continuous)
            nh_units: number of units in the hidden layer
            activation_fun: a function passed in to serve as the activation function
                for the network
            max_epochs: maximum number of times the algorithm passes through all
                rows of X
            mse_threshold: lower bound on Mean Squared Error - if the model achieves
                an MSE below this threshold, training will end there
            lr: the learning rate - controls how quickly the algorithm may converge
        """

        # Set activation_fun
        self.activation_fun = activation_fun

        # Initialize weights
        w1 = np.random.normal(scale = .01, size = [2, nh_units])
        w2 = np.random.normal(scale = .01, size = nh_units + 1)

        # Initialize i
        i = 0
        mse_above_threshold = True

        # Using stochastic gradient descent, solve for the weights
        while i <= max_epochs and mse_above_threshold:
            # Iterate through all training points
            for j in range(len(y)):
                # Select point for evaluation
                X_i = X[j]
                y_i = y[j]

                # Add bias to x
                X_i = np.array([1,X_i])

                # Input layer to hidden layer
                hl = self.activation_fun(np.dot(X_i, w1))

                # Add bias to hidden layer
                hl = np.insert(hl, 0, 1)

                # Hidden layer to output layer
                ol = np.dot(hl, w2)

                # Now output has been calculated - time to backpropogate
                # Calculate gradient with respect to w1
                w1_grad = (2*(ol - y_i)) * w2[1:] * (1 - hl[1:]**2) * np.expand_dims(X_i, 1)

                # Update w1
                w1 -= (lr * w1_grad)

                # Calculate gradient with respect to w2
                w2_grad = (2 * (ol - y_i)) * (hl)

                # Update w2
                w2 -= (lr * w2_grad)

            # Save updated weights
            self.weights = [w1, w2]

            # Calculate and report error
            self.y_pred = self.predict(X)

            out_mse = np.mean((self.y_pred - y)**2)

            # Save MSE metrics
            self.mse_log.append(out_mse)
            self.mse = out_mse

            # Save i
            self.epochs = i

            # Update i and mse_above_threshold
            i += 1
            mse_above_threshold = self.mse > mse_threshold

        return self

    def predict(self, X):
        """
        Creates predictions based on a trained model
        Args:
            X: numpy array of features

        Returns:
            numpy array of predicted values based on given X
        """

        X = np.c_[np.ones(len(X)), X]
        s1 = self.activation_fun(np.dot(X, self.weights[0]))
        s1 = np.c_[np.ones(X.shape[0]), s1]
        y_pred = np.dot(s1, self.weights[1])
        return y_pred

    def plot_mse(self):
        """
        Plots the Mean Squared Error (MSE) of the algorithm in relation to the
        number of epochs.
        """

        plt.plot(range(self.epochs), self.mse_log)
        plt.xlabel("Epochs")
        plt.ylabel("MSE")
        plt.title("MSE by Epoch")
        plt.show()
