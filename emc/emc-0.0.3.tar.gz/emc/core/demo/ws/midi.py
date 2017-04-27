from matplotlib.pyplot import *
from numpy import arange


if __name__ == '__main__':
    
    pitches       = [60, 62, 64, 66]
    onsets        = [0,  2,  3,  6]
    durations     = [7,  2,  2,  2]
    
    for i in range(len(pitches)):
        gca().add_patch(Rectangle((onsets[i], pitches[i] - .5), durations[i], 1, facecolor='#703020'))
    
    grid('on')
    xlim((-1, 9))
    ylim((57, 69))
    xticks(arange(0,9))
    yticks(arange(57,70))
    xlabel('Time (ticks)', fontsize=20)
    ylabel('Pitch (MIDI key)', fontsize=20)
    
    tight_layout()
    #savefig('midi.pdf')
        
    show()