from matplotlib.pyplot import *
from numpy import *

p1 = array([.1, .15, .18, .22, .32, .75, .77, .81])
p2 = array([.7, .25, .18, .82, .22, .65, .77, .81])

t1 = 0.35
t2 = 0.75

def setUpFigure():
    fig = figure()
    plot(p1, p2, 'x', color='#603000', markersize=8, markeredgewidth=1.5, label='Corpus members')
    plot(t1, t2, 'o', color='#006030', markersize=11, label='Tested model')
    xlabel('Property 0', fontsize=20)
    ylabel('Property 1', fontsize=20)
    xlim([0, 1])
    ylim([0, 1])
    return fig


def finalizeFigure(filename):
    legend(loc=4, fontsize=18, numpoints=1)
    #savefig(filename)
    

if __name__ == '__main__':
    # FIG 1 - SETUP
    setUpFigure()
    finalizeFigure('clustering1.pdf')
    
    # FIG 2 - MEAN
    setUpFigure()
    plot(mean(p1), mean(p2), '*', color='#703080', markersize=15, label='Corpus centre')
    plot([mean(p1), t1], [mean(p2), t2], ':', color='#909090')
    finalizeFigure('clustering2.pdf')
    
    # FIG 3 - CLOSEST
    setUpFigure()
    plot([p1[3], t1], [p2[3], t2], ':', color='#909090')
    plot(p1[3], p2[3], '*', color='#703080', markersize=15, label='Closest corpus member')
    finalizeFigure('clustering3.pdf')
    
    # FIG 4 - CLUSTER
    fig = setUpFigure()
    c11 = mean(p1[[0,3]])
    c12 = mean(p2[[0,3]])
    c21 = mean(p1[[1,2,4]])
    c22 = mean(p2[[1,2,4]])
    c31 = mean(p1[[5,6,7]])
    c32 = mean(p2[[5,6,7]])
    plot([c11,c21,c31], [c12,c22,c32], '*', color='#703080', markersize=15, label='Cluster centres')
    plot([c11, t1], [c12, t2], ':', color='#909090')
    
    fig.gca().add_artist(Circle((c11,c12), 0.13, color=(.25,0,0,.05)))
    fig.gca().add_artist(Circle((c21,c22), 0.15, color=(0,.25,0,.05)))
    fig.gca().add_artist(Circle((c31,c32), 0.15, color=(0,0,.25,.05)))
    finalizeFigure('clustering4.pdf')
    show()