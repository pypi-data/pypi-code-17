# This is a python implementation of the ForceAtlas2 plugin from Gephi
# intended to be used with networkx, but is in theory independent of
# it since it only relies on the adjacency matrix.  This
# implementation is based directly on the Gephi plugin:
#
# https://github.com/gephi/gephi/blob/master/modules/LayoutPlugin/src/main/java/org/gephi/layout/plugin/forceAtlas2/ForceAtlas2.java
#
# This is in contrast to an implementation I found in R (which uses
# strange parametrization) and to one in Python (which is based on the
# spring_layout).  The python implementation did not seem to work, and
# I did not try the R implementation because I didn't want to spend a
# long time setting up a messy pipe system only to find that the
# algorithm was as wrong as the python one.
#
# For simplicity and for keeping code in sync with upstream, I have
# reused as many of the variable/function names as possible, even when
# they are in a more java-like style (e.g. camalcase)
#
# I wrote this because I was unable to find a graph layout algorithm
# in Python that clearly showed modular structure.
#
# NOTES: Currently, this only works for unweighted, undirected graphs.
#
# Copyright 2016 Max Shinn <mws41@cam.ac.uk>
#
# Available under the GPLv3

"""
Author: Max Shinn 2016
Modified on 20.4.17, Lenz Baumann
E-Mail: lnzbmnn@gmail.com
"""

import random
from math import sqrt

import numpy

from communitweet import fa2util


def forceatlas2(
        G,  # a graph, in 2D numpy ndarray format
        pos=None,  # Vector of initial positions
        niter=100,  # Number of times to iterate the main loop

        # Behavior alternatives
        outboundAttractionDistribution=False,  # "Dissuade hubs" # NOT (fully) IMPLEMENTED
        linlogMode=False,
        adjustSizes=False,
        edgeWeightInfluence=1,

        # Performance
        jitterTolerance=1.0,  # "Tolerance"

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=1.0,
        sizes=None
):
    # Check our assumptions
    assert isinstance(G, numpy.ndarray), "G is not a numpy ndarray"
    assert G.shape == (G.shape[0], G.shape[0]), "G is not 2D square"
    assert numpy.all(G.T == G), "G is not symmetric.  Currently only undirected graphs are supported"
    assert isinstance(pos, numpy.ndarray) or (pos is None), "Invalid node positions"
    assert len(G) > 0, "Graph is empty"
    # assert outboundAttractionDistribution == linLogMode == adjustSizes == barnesHutOptimize == False, "You selected a feature that has not been implemented yet..."



    # Initializing, ala initAlgo()
    # ============================

    # speed and speedEfficiency describe a scaling factor of dx and dy
    # before x and y are adjusted.  These are modified as the
    # algorithm runs to help ensure convergence.
    speed = 1
    speedEfficiency = 1

    # Put nodes into a data structure we can understand
    nodes = []

    for i in range(0, G.shape[0]):
        n = fa2util.Node()
        n.mass = 1 + numpy.sum(G[i])
        n.old_dx = 0
        n.old_dy = 0
        n.dx = 0
        n.dy = 0
        if sizes is not None:
            n.size = int(sizes[i])
        if pos is None:
            n.x = random.random()
            n.y = random.random()
        else:
            n.x = pos[i][0]
            n.y = pos[i][1]
        nodes.append(n)

    # Put edges into a data structure we can understand
    edges = []
    es = numpy.asarray(G.nonzero()).T
    for e in es:  # Iterate through edges
        if e[1] <= e[0]: continue  # Avoid duplicate edges
        edge = fa2util.Edge()
        edge.node1 = e[0]  # The index of the first node in `nodes`
        edge.node2 = e[1]  # The index of the second node in `nodes`
        edge.weight = G[tuple(e)]
        edges.append(edge)

    # Main loop, i.e. goAlgo()
    # ========================

    # Each iteration of this loop reseprensts a call to goAlgo().

    helper_ind = 0
    for _i in range(0, niter):
        #helper_ind+=1
        #print(str(helper_ind/niter*100))
        for n in nodes:
            n.old_dx = n.dx
            n.old_dy = n.dy
            n.dx = 0
            n.dy = 0

        # Barnes Hut optimization step goes here...

        if outboundAttractionDistribution:
            outboundAttCompensation = numpy.mean([n.mass for n in nodes])

        fa2util.apply_repulsion(nodes, scalingRatio, adjustSizes=adjustSizes)
        fa2util.apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=strongGravityMode, adjustSizes=adjustSizes)
        fa2util.apply_attraction(nodes, edges, scalingRatio, edgeWeightInfluence, adjustSizes=adjustSizes, linlogMode=linlogMode)

        # Auto adjust speed.
        totalSwinging = 0.0  # How much irregular movement
        totalEffectiveTraction = 0.0  # How much useful movement
        for n in nodes:
            swinging = sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
            totalSwinging += n.mass * swinging
            totalEffectiveTraction += .5 * n.mass * sqrt(
                (n.old_dx + n.dx) * (n.old_dx + n.dx) + (n.old_dy + n.dy) * (n.old_dy + n.dy))

        # Optimize jitter tolerance.  The 'right' jitter tolerance for
        # this network. Bigger networks need more tolerance. Denser
        # networks need less tolerance. Totally empiric.
        estimatedOptimalJitterTolerance = .05 * sqrt(len(nodes))
        minJT = sqrt(estimatedOptimalJitterTolerance)
        maxJT = 10
        jt = jitterTolerance * max(minJT, min(maxJT, estimatedOptimalJitterTolerance * totalEffectiveTraction / (
            len(nodes) * len(nodes))))

        minSpeedEfficiency = 0.05

        if totalSwinging / totalEffectiveTraction > 2.0:
            if speedEfficiency > minSpeedEfficiency:
                speedEfficiency *= .5
            jt = max(jt, jitterTolerance)

        targetSpeed = jt * speedEfficiency * totalEffectiveTraction / totalSwinging

        if totalSwinging > jt * totalEffectiveTraction:
            if speedEfficiency > minSpeedEfficiency:
                speedEfficiency *= .7
        elif speed < 1000:
            speedEfficiency *= 1.3

        maxRise = .5
        speed = speed + min(targetSpeed - speed, maxRise * speed)

        if adjustSizes:
            for n in nodes:
                swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
                factor = 0.1 * speed / (1.0 + sqrt(speed * swinging))
                df = sqrt(pow(n.dx, 2) + pow(n.dy, 2))
                factor = min(factor * df, 10.0) / df
                n.x += n.dx * factor
                n.y += n.dy * factor
        else:
            for n in nodes:
                swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
                factor = speed / (1.0 + sqrt(speed * swinging))
                n.x += n.dx * factor
                n.y += n.dy * factor
    return [(n.x, n.y) for n in nodes]


def forceatlas2_networkx_layout(G, pos=None, sizes=None, **kwargs):
    import networkx
    assert isinstance(G, networkx.classes.graph.Graph), "Not a networkx graph"
    assert isinstance(pos, dict) or (pos is None), "pos must be specified as a dictionary, as in networkx"
    M = numpy.asarray(networkx.to_numpy_matrix(G))
    if pos is None:
        l = forceatlas2(M, pos=None, sizes=sizes, **kwargs)
    else:
        poslist = numpy.asarray([pos[i] for i in G.nodes()])
        l = forceatlas2(M, pos=poslist, **kwargs)
    return dict(zip(G.nodes(), l))
