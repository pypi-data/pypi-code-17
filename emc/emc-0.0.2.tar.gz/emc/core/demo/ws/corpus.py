from matplotlib.pyplot import *
from numpy import *

from emc.core.integ.modeldir import ModelDirectory
from emc.cpp.wrapper.descriptor import DescriptorDirectoryWrapper, numDescriptors


if __name__ == '__main__':
    
    md = ModelDirectory('../../../../midi/bach_1track')
    md2 = ModelDirectory('../../../../midi/bach_2track')
    dd = DescriptorDirectoryWrapper(md, numClusters = 1)
    dd2 = DescriptorDirectoryWrapper(md2, numClusters = 1)
    
    cd  = dd.centreDescriptors()
    cd2 = dd2.centreDescriptors()
    cd.shape  = (numDescriptors, 128)
    cd2.shape = (2, numDescriptors, 128)
    
    
    
    # fig 1 - centre pitch histogram
    
    figure()
    plot(cd[8, :], color='#502010')
    
    grid('on')
    xticks(arange(0,129,16))
    xlabel('Pitch value', fontsize=20)
    ylabel('Number of occurrences', fontsize=20)
    tight_layout()
    
    #savefig('pitchhistcorpus.pdf')
    show()
    '''
    
    # fig 2 - centre pitch differential histogram
    
    figure()
    plot(arange(-64,64), cd[9, :], color='#502010')
    
    grid('on')
    xticks(arange(-64,64,16))
    xlabel('Pitch change rate', fontsize=20)
    ylabel('Number of occurrences', fontsize=20)
    tight_layout()
    
    #savefig('pitchdiffhistcorpus.pdf')
    
    
    # fig 3 - centre pitch histogram mono vs. stereo
    
    x = arange(128)
    pitch_hist = cd[8, :]
    pitch_hist_L = cd2[0, 8, :]
    pitch_hist_R = cd2[1, 8, :]
    
    figure()
    plot(pitch_hist, linestyle='-', color=(0.25, 0.15, 0.1))
    fill_between(x, pitch_hist, where = pitch_hist>=0, color=(0.45, 0.25, 0.2, 0.3))
    
    grid('on')
    xticks(arange(0,129,16))
    xlabel("Pitch value", fontsize=20)
    ylabel("Number of occurences", fontsize=20)
    tight_layout()
    
    #savefig('pitchhistcorpus2a.pdf')
    
    figure()
    plot(pitch_hist_L, linestyle='-', color=(0.1, 0.25, 0.15), label='Dual-track 1')
    fill_between(x, pitch_hist_L, where = pitch_hist_L>=0, color=(0.2, 0.45, 0.25, 0.3))
    plot(pitch_hist_R, linestyle='-', color=(0.15, 0.1, 0.25), label='Dual-track 2')
    fill_between(x, pitch_hist_R, where = pitch_hist_R>=0, color=(0.25, 0.2, 0.45, 0.3))
    
    grid('on')
    xticks(arange(0,129,16))
    xlabel("Pitch value", fontsize=20)
    ylabel("Number of occurences", fontsize=20)
    tight_layout()
    
    #savefig('pitchhistcorpus2b.pdf')
    show()
    
    
    # fig 4 - centre pitch histogram mono vs. stereo
    
    figure()
    x = arange(-64,64)
    pitch_hist = cd[9, :]
    pitch_hist_L = cd2[0, 9, :]
    pitch_hist_R = cd2[1, 9, :]
    
    plot(x, pitch_hist, '_', markersize=6, linestyle='-', color=(0.25, 0.15, 0.1), label='Single track')
    fill_between(x, pitch_hist, where = pitch_hist>=0, color=(0.45, 0.25, 0.2, 0.3))
    plot(x, pitch_hist_L, '+', markersize=6, linestyle='-', color=(0.1, 0.25, 0.15), label='Dual track 1')
    fill_between(x, pitch_hist_L, where = pitch_hist_L>=0, color=(0.2, 0.45, 0.25, 0.3))
    plot(x, pitch_hist_R, 'x', markersize=6, linestyle='-', color=(0.15, 0.1, 0.25), label='Dual track 2')
    fill_between(x, pitch_hist_R, where = pitch_hist_R>=0, color=(0.25, 0.2, 0.45, 0.3))
    
    #title("Mean of the pitch distribution of the corpus")
    legend(fontsize=18)
    grid('on')
    xticks(arange(-64,64,16))
    xlabel("Pitch change rate", fontsize=20)
    ylabel("Number of occurences", fontsize=20)
    tight_layout()
    
    #savefig('pitchdiffhistcorpus2.pdf')
    '''
    
    
    # fig 5 - inter-onset interval FFT of one
    '''
    ioi = zeros(508, dtype=uint16)
    ioi[:] = md.models[0].interonsets()
    pf = dd.diffFourier(ioi, 128, False)
    
    figure()
    plot(arange(pi/128,pi+pi/128,pi/128), pf, color='#502010')
    
    grid('on')
    
    T = array([8,7,6,5,4,3,2,1], dtype=uint8)
    omega = (2 * pi / T) % (2 * pi)
    xticks(omega)
    gca().set_xticklabels(['$\\frac{2\pi}{8}$',
                           '$\\frac{2\pi}{7}$',
                           '$\\frac{2\pi}{6}$',
                           '$\\frac{2\pi}{5}$',
                           '$\\frac{2\pi}{4}$',
                           '$\\frac{2\pi}{3}$',
                           '$\\frac{2\pi}{2}$',
                           '0'])
    for tick in gca().xaxis.get_major_ticks()[:-1]:
        tick.label.set_fontsize(20)
    
    xlabel('Inter-onset interval frequency', fontsize=20)
    ylabel('FFT value', fontsize=20)
    xlim([-0.1, pi+0.1])
    tight_layout()
    
    #savefig('ioifftcorpus.pdf')
    show()
    '''