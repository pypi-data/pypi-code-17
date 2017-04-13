import numpy as np
import matplotlib.pyplot as plt

def mplot(data, target, classification=True, filename=None):
    '''
    Visualizes many-dimensional data to identify a model. 
    
    :param data: Matrix of features with shape (n_samples, n_features)
    :type data: np.ndarray
    :param target: 1D array of labels with shape (n_samples,)
    :type target: np.ndarray
    :param classification: If True, labels are intepreted as discrete; otherwise, labels are interpreted as continuous
    :type classification: bool
    :param filename: If provided, saves the plot as an image to 'filename.png'; otherwise, plot is displayed to the screen
    :type filename: str
    '''
    count = data.shape[1]
    
    fig = plt.figure(figsize=(count*6,count*4))
    if classification:
        target_range = np.unique(target)
    else:
        target_range = np.linspace(target.min(), target.max(), 65)

    for i in xrange(count):
        for j in xrange (count):
            plt.subplot(count, count, i*count+j+1)
            if i != j:
                plt.scatter(data[:,i],data[:, j],c=target)
            else:
                plt.text(0,0,str(i), fontdict={'size':40})
                plt.colorbar(mappable=plt.contourf(np.vstack(target_range)))
                
    if filename != None:
        plt.savefig(filename + '.png', bbox_inches=0)
    else:
        plt.show()
