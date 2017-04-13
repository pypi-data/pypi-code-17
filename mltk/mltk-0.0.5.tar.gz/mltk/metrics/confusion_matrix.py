"""
The Confusion Matrix class exposes numerous statistics critical to evaluating an 
:math:`n`-class model. Matrices are initialized with the number of classes, and 
batch add operations can be performed with the `add` function. Numerous statistics
with their default acronyms can additionally be accessed. 
"""
import numpy as np

class ConfusionMatrix:
    """
    Defines the confusion matrix class for :math:`n` distinct classes (enumeration agnostic).
    """
    def __init__(self, n_classes):
        '''
        :param n_classes: integer representing the number of classes in the input data to perform :math:`n`-class statistical analysis
        '''
        self.n_classes = n_classes
        self.mat = np.zeros((n_classes,n_classes), dtype='int')
        self.lista = np.array(())
        self.listb = np.array(())

    def __str__(self):
        '''        
        :return: a string representation of the internal class matrix
        '''
        return np.array_str(self.mat)

    def add(self, y_true, y_pred):
        '''
        Adds the arrays y_true and y_pred to the confusion matrix in a batch format

        :param y_true: The true distribution of classes
        :param y_pred: The predicted distribution of classes
        '''
        assert len(y_true) == len(y_pred)
        assert max(y_true) < self.n_classes
        assert max(y_pred) < self.n_classes

        self.lista = np.append(self.lista, np.asarray(y_true)).flatten()
        self.listb = np.append(self.listb, np.asarray(y_pred)).flatten()

        for i in range(len(y_true)):
            self.mat[y_true[i],y_pred[i]] += 1

    def zero(self):
        '''
        Resets the internal confusion matrix (but does *not* change the y_true and y_pred arrays)
        ''' 
        self.mat.fill(0)
    
    def ratings(self):
        '''
        
        :return: The internal stored y_true and y_pred arrays as a single np.array
        '''
        return np.array([self.lista, self.listb])

    def errors(self):
        '''
        Calculates different error types associated with the confusion matrix

        :return: Vectors of true postives (tp) false negatives (fn), false positives (fp) and true negatives (tn). 
                 In this case, pos 0 is first class, pos 1 is second class, etc.
        '''
        tp = np.asarray(np.diag(self.mat).flatten(),dtype='float')
        fn = np.asarray(np.sum(self.mat, axis=1).flatten(),dtype='float') - tp
        fp = np.asarray(np.sum(self.mat, axis=0).flatten(),dtype='float') - tp
        tn = np.asarray(np.sum(self.mat)*np.ones(self.n_classes).flatten(),dtype='float') - tp - fn - fp
        return tp, fn, fp, tn

    def accuracy(self):
        '''
        Calculates the accuracy of classification given the stored matrix representation

        :return: A numerical accuracy value associated with the confusion matrix
        '''
        tp, _, _, _ = self.errors()
        n_samples = np.sum(self.mat)
        return np.sum(tp) / n_samples

    def sensitivity(self):
        '''
        Calculates the sensitivity of classification given the stored matrix representation

        :return: A sensitivity vector including all classes associated with the confusion matrix
        '''
        tp, tn, fp, fn = self.errors()
        res = tp / (tp + fn)
        res = res[~np.isnan(res)]
        return res

    def specificity(self):
        '''
        Calculates the specificity of classification given the stored matrix representation

        :return: A specificity vector including all classes associated with the confusion matrix
        '''        
        tp, tn, fp, fn = self.errors()
        res = tn / (tn + fp)
        res = res[~np.isnan(res)]
        return res

    def ppv(self):
        '''
        Calculates the positive predictive value (or precision) of classification given the stored matrix representation

        :return: A PPV vector including all classes associated with the confusion matrix
        '''           
        tp, tn, fp, fn = self.errors()
        res = tp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def npv(self):
        '''
        Calculates the negative predictive value of classification given the stored matrix representation

        :return: A NPV vector including all classes associated with the confusion matrix
        '''          
        tp, tn, fp, fn = self.errors()
        res = tn / (tn + fn)
        res = res[~np.isnan(res)]
        return res

    def fpr(self):
        '''
        Calculates the false positive rate (or fall-out) of classification given the stored matrix representation

        :return: A FPR vector including all classes associated with the confusion matrix
        '''  
        tp, tn, fp, fn = self.errors()
        res = fp / (fp + tn)
        res = res[~np.isnan(res)]
        return res

    def fdr(self):
        '''
        Calculates the false discovery rate of classification given the stored matrix representation

        :return: A FDR vector including all classes associated with the confusion matrix
        ''' 
        tp, tn, fp, fn = self.errors()
        res = fp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def f1(self):
        '''
        Calculates the f1-score (the harmonic mean of precision and sensitivity) of classification given the stored matrix representation

        :return: A f1 vector including all classes associated with the confusion matrix
        '''         
        tp, tn, fp, fn = self.errors()
        res = (2*tp) / (2*tp + fp + fn)
        res = res[~np.isnan(res)]
        return res

    def prevalence(self):
        '''
        Calculates the prevalence of classification given the stored matrix representation

        :return: A prevalence vector including all classes associated with the confusion matrix
        ''' 
        tp, tn, fp, fn = self.errors()
        res = (tp + fn) / (tp + fn + fp + tn)
        res = res[~np.isnan(res)]
        return res

    def matthews_correlation(self):
        '''
        Calculates the matthews correlation coefficient of classification given the stored matrix representation

        :return: A MCC vector including all classes associated with the confusion matrix
        '''         
        tp, tn, fp, fn = self.errors()
        numerator = tp*tn - fp*fn
        denominator = np.sqrt((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn))
        res = numerator / denominator
        res = res[~np.isnan(res)]
        return res

    def matrix(self):
        '''

        :return: The internal matrix representation of the ConfusionMatrix class
        ''' 
        return self.mat

    def binary_pretty_print(self, class_labels=['0','1'], plot=False): 
        '''
        Provides a visualization of a binary confusion matrix with class labels, associated metrics, and enumerated counts

        :param class_labels: optional (default [0, 1]), labels the classes for the visualization
        :param plot: optional (default False), plots the matrix if True
        :return: A matplotlib object representing the binary confusion matrix
        '''

        from sklearn.metrics import confusion_matrix
        import matplotlib.pyplot as plt
        
        C = confusion_matrix(self.lista, self.listb)

        assert C.shape == (2,2), "Confusion matrix should be from binary classification only."
        
        tn = C[0,0]; fp = C[0,1]; fn = C[1,0]; tp = C[1,1];

        NP = fn+tp
        NN = tn+fp
        N  = NP+NN

        fig = plt.figure(figsize=(8,8))
        ax  = fig.add_subplot(111)
        ax.imshow(C, interpolation='nearest', cmap=plt.cm.gray)

        # Draw the grid boxes
        ax.set_xlim(-0.5,2.5)
        ax.set_ylim(2.5,-0.5)
        ax.plot([-0.5,2.5],[0.5,0.5], '-k', lw=2)
        ax.plot([-0.5,2.5],[1.5,1.5], '-k', lw=2)
        ax.plot([0.5,0.5],[-0.5,2.5], '-k', lw=2)
        ax.plot([1.5,1.5],[-0.5,2.5], '-k', lw=2)

        # Set xlabels
        ax.set_xlabel('Predicted Label', fontsize=16)
        ax.set_xticks([0,1,2])
        ax.set_xticklabels(class_labels + [''])
        ax.xaxis.set_label_position('top')
        ax.xaxis.tick_top()
        ax.xaxis.set_label_coords(0.34,1.06)

        # Set ylabels
        ax.set_ylabel('True Label', fontsize=16, rotation=90)
        ax.set_yticklabels(class_labels + [''],rotation=90)
        ax.set_yticks([0,1,2])
        ax.yaxis.set_label_coords(-0.09,0.65)


        ax.text(
                0, 0,
                'True Neg: %d\n(Num Neg: %d)'%(tn,NN),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(0,1,
                'False Neg: %d'%fn,
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(1,0,
                'False Pos: %d'%fp,
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))


        ax.text(1,1,
                'True Pos: %d\n(Num Pos: %d)'%(tp,NP),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(2,0,
                'False Pos Rate: %.2f'%(fp / (fp+tn+0.)),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(2,1,
                'True Pos Rate: %.2f'%(tp / (tp+fn+0.)),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(2,2,
                'Accuracy: %.2f'%((tp+tn+0.)/N),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(0,2,
                'Neg Pre Val: %.2f'%(1-fn/(fn+tn+0.)),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))

        ax.text(1,2,
                'Pos Pred Val: %.2f'%(tp/(tp+fp+0.)),
                va='center',
                ha='center',
                bbox=dict(fc='w',boxstyle='round,pad=1'))


        plt.tight_layout()

        if plot:
            plt.show()

        return plt
