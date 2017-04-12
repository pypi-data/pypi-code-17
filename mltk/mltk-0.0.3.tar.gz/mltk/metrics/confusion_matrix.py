import numpy as np

class ConfusionMatrix:

    def __init__(self, n_classes):
        self.n_classes = n_classes
        self.mat = np.zeros((n_classes,n_classes), dtype='int')
        self.lista = np.array(())
        self.listb = np.array(())

    def __str__(self):
        return np.array_str(self.mat)

    def add(self, y_true, y_pred):
        assert len(y_true) == len(y_pred)
        assert max(y_true) < self.n_classes
        assert max(y_pred) < self.n_classes

        self.lista = np.append(self.lista, np.asarray(y_true)).flatten()
        self.listb = np.append(self.listb, np.asarray(y_pred)).flatten()

        for i in range(len(y_true)):
                self.mat[y_true[i],y_pred[i]] += 1

    def zero(self):
        self.mat.fill(0)
    
    def ratings(self):
        return np.array([self.lista, self.listb])

    def errors(self):
        """
        Calculate different error types
        :return: vetors of true postives (tp) false negatives (fn), false positives (fp) and true negatives (tn)
                 pos 0 is first class, pos 1 is second class etc.
        """
        tp = np.asarray(np.diag(self.mat).flatten(),dtype='float')
        fn = np.asarray(np.sum(self.mat, axis=1).flatten(),dtype='float') - tp
        fp = np.asarray(np.sum(self.mat, axis=0).flatten(),dtype='float') - tp
        tn = np.asarray(np.sum(self.mat)*np.ones(self.n_classes).flatten(),dtype='float') - tp - fn - fp
        return tp, fn, fp, tn

    def accuracy(self):
        tp, _, _, _ = self.errors()
        n_samples = np.sum(self.mat)
        return np.sum(tp) / n_samples

    def sensitivity(self):
        tp, tn, fp, fn = self.errors()
        res = tp / (tp + fn)
        res = res[~np.isnan(res)]
        return res

    def specificity(self):
        tp, tn, fp, fn = self.errors()
        res = tn / (tn + fp)
        res = res[~np.isnan(res)]
        return res

    def ppv(self):
        tp, tn, fp, fn = self.errors()
        res = tp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def npv(self):
        tp, tn, fp, fn = self.errors()
        res = tn / (tn + fn)
        res = res[~np.isnan(res)]
        return res

    def fpr(self):
        tp, tn, fp, fn = self.errors()
        res = fp / (fp + tn)
        res = res[~np.isnan(res)]
        return res

    def fdr(self):
        tp, tn, fp, fn = self.errors()
        res = fp / (tp + fp)
        res = res[~np.isnan(res)]
        return res

    def f1(self):
        tp, tn, fp, fn = self.errors()
        res = (2*tp) / (2*tp + fp + fn)
        res = res[~np.isnan(res)]
        return res

    def prevalence(self):
        tp, tn, fp, fn = self.errors()
        res = (tp + fn) / (tp + fn + fp + tn)
        res = res[~np.isnan(res)]
        return res

    def matthews_correlation(self):
        tp, tn, fp, fn = self.errors()
        numerator = tp*tn - fp*fn
        denominator = np.sqrt((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn))
        res = numerator / denominator
        res = res[~np.isnan(res)]
        return res

    def matrix(self):
        return self.mat

    def binary_pretty_print(self, class_labels=['0','1']): 
        '''
        Improves the built-in sklearn confusion matrix with associated values
        C: np.ndarray, shape (2, 2) as given by sklearn's confusion_matrix
        '''

        from sklearn.metrics import confusion_matrix
        import matplotlib.pyplot as plt
        import numpy as np
        
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


        ax.text(0,0,
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
        return plt