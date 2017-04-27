from matplotlib.pyplot import *
from numpy import *
from numpy.matlib import repmat

from emc.core.integ.modeldir import ModelDirectory
from emc.cpp.wrapper.descriptor import DescriptorDirectoryWrapper


if __name__ == '__main__':
    pitches = array([60, 62, 64, 62], dtype=uint16)
    pitches = repmat(pitches, 1, 256)[0]
    
    md = ModelDirectory('../../../../../../midi/bach_1track')
    dd = DescriptorDirectoryWrapper(md, numClusters = 1)
    pf = dd.fourier(pitches, 128, False)
    
    
    figure()
    for i in range(10):
        gca().add_patch(Rectangle((i, pitches[i] - .5), 1, 1, facecolor='#703020'))
    
    grid('on')
    xlim([-1, 11])
    ylim([55, 67])
    xticks(arange(-1,12))
    yticks(arange(55,68))
    xlabel('Time (ticks)', fontsize=20)
    ylabel('Pitch (MIDI key)', fontsize=20)
    
    tight_layout()
    #savefig('descriptorspectrum1.pdf')
    
    
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
    #savefig('descriptorspectrum2.pdf')
    show()