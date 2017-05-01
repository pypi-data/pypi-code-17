#
# This file is part of TransportMaps.
#
# TransportMaps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TransportMaps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TransportMaps.  If not, see <http://www.gnu.org/licenses/>.
#
# Transport Maps Library
# Copyright (C) 2015-2017 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Author: Transport Map Team
# Website: transport-maps.mit.edu
# Support: transport-maps.mit.edu/qa/
#

import copy
import warnings
import numpy as np
import scipy.stats as scistat
try:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
except ImportError:
    PLOT_SUPPORT = False
    warnings.warn("Plotting support disabled: install matplotlib.")
else:
    PLOT_SUPPORT = True

from TransportMaps import mpi_eval, logger
import TransportMaps as TM
import TransportMaps.Maps as MAPS
import TransportMaps.Distributions as DIST

__all__ = ['AlignedConditionalsObject', 'computeAlignedConditionals',
           'plotAlignedConditionals',
           'RandomConditionalsObject', 'computeRandomConditionals',
           'plotRandomConditionals',
           'plotAlignedSliceMap', 'plotAlignedMarginals',
           'plotGradXMap', 'plotLinearityMap', 'niceSpy']

def frexp10(x,numdecimals=1):  #Returns mantissa and exponent of a given number
    exp = int( np.floor( np.log10(x) ) )
    factor = 10.**(numdecimals)
    mant =   x / 10.**exp
    return mant, exp

class AlignedConditionalsObject(TM.TMO):
    def __init__(self, nplots, X_list, Y_list, pdfEval_list):
        self.nplots = nplots
        self.X_list = X_list
        self.Y_list = Y_list
        self.pdfEval_list = pdfEval_list

def computeAlignedConditionals(distribution, dimensions_vec=0, pointEval=None,
                               range_vec=[-3,3], numPointsXax = 30,
                               mpi_pool=None):
    r""" Compute the conditionals aligned with the axis

    Args:
      distribution (:class:`Distribution<Distribution>`): distribution :math:`\pi`
      dimensions_vec (list of int): list of dimensions to be displayed. Default 0: display
        10 dimensions at most.
      pointEval (:class:`ndarray<numpy.ndarray>` [:math:`d`]): anchor point.
        Default is zero.
      range_vec (:class:`list<list>`): range to be displayed. Either a
        :class:`list<list>` [2] of integers, or a :class:`list<list>` [d] of
        :class:`list<list>` [2] of integers.
      numPointsXax (int): number of points for each axis.
      mpi_pool (:class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`): pool of processes

    Returns:
      (:class:`AlignedConditionalsObject<AlignedConditionalsObject>`) -- object
        storing all the necessary evaluated values
    """
    dim = distribution.dim
    #Assign optional parameters if not defined
    if dimensions_vec == 0:
        dimensions_vec = list(range( min(dim,30) ))
    else:
        dimensions_vec = list(dimensions_vec)
    if pointEval is None:
       pointEval = np.zeros(dim)
    nplots = len(dimensions_vec) # number of subplots per dimension
    # Prepare range_vec
    if not isinstance(range_vec[0], list):
        range_vec = [range_vec] * distribution.dim
    
    # Create list of points for every 2d plot
    X_list = []
    Y_list = []
    tempMat_list = []
    for ii in range(nplots):
        for jj in range(ii+1):
            if jj<ii: # 2d plot
                #The x variable is jj, whereas the y-variable is ii.
                #Create evaluation grid
                xlin = np.linspace( range_vec[jj][0] , range_vec[jj][1],
                                    num=numPointsXax) + \
                       pointEval[jj] #Notice x -- jj
                ylin = np.linspace( range_vec[ii][0] , range_vec[ii][1],
                                    num=numPointsXax) + \
                       pointEval[ii]
                X, Y = np.meshgrid(xlin, ylin)
                X_eval = X.flat #Flat iterator over the array
                Y_eval = Y.flat
                #Slice 2d pdf
                npointEval =len(X_eval) #Number of points where to evaluate the slice
                tempMat = np.tile(pointEval,(npointEval,1))
                tempMat[:,dimensions_vec[ii]] = Y_eval
                tempMat[:,dimensions_vec[jj]] = X_eval
                # Append
                X_list.append(X)
                Y_list.append(Y)
                tempMat_list.append(tempMat)

    # Create list of points for every 1d plot
    for jj in range(nplots):  #1D plot
        xlin = np.linspace( range_vec[jj][0] , range_vec[jj][1],
                            num=numPointsXax) + pointEval[jj]
        #Slice 1d pdf
        npointEval =len(xlin) #Number of points where to evaluate the slice
        tempMat = np.tile(pointEval,(npointEval,1))
        tempMat[:,dimensions_vec[jj]] = xlin
        # Append
        X_list.append(xlin)
        tempMat_list.append(tempMat)

    # Evaluate
    npoints_list = [0] + [ tmat.shape[0] for tmat in tempMat_list ]
    npoints_pos = np.cumsum(npoints_list)
    tempMat_mat = np.concatenate(tempMat_list, axis=0)
    scatter_tuple = (['x'], [tempMat_mat])
    pdfEval_mat = mpi_eval("pdf", obj=distribution, scatter_tuple=scatter_tuple,
                           mpi_pool=mpi_pool)
    pdfEval_list = [ pdfEval_mat[npoints_pos[i]:npoints_pos[i+1]]
                     for i in range(len(tempMat_list)) ]

    data = AlignedConditionalsObject(nplots, X_list, Y_list, pdfEval_list)
    return data
    
def plotAlignedConditionals(distribution=None, data=None, dimensions_vec=0, pointEval=None,
                            range_vec=[-3,3], numPointsXax = 30, numCont = 15,
                            figname=None, show_flag=True,
                            show_title=False,
                            title='Aligned conditionals',
                            vartitles=None,
                            fig=None,
                            mpi_pool=None):
    r""" Plot the conditionals aligned with the axis

    Args:
      distribution (:class:`Distribution<Distribution>`): distribution :math:`\pi`
      data (:class:`AlignedConditionalsObject`): output of :func:`computeAlignedConditionals`
      dimensions_vec (list of int): list of dimensions to be displayed. Default 0: display
        10 dimensions at most.
      pointEval (:class:`ndarray<numpy.ndarray>` [:math:`d`]): anchor point.
        Default is zero.
      range_vec (:class:`list<list>`): range to be displayed. Either a
        :class:`list<list>` [2] of integers, or a :class:`list<list>` [d] of
        :class:`list<list>` [2] of integers.
      numPointsXax (int): number of points for each axis.
      numCont (int): number of contours in the contour plots.
      figname (str): if defined, store the figure in the provided path.
      show_flag (bool): whether to show the plot before returning
      show_title (bool): whether to show the title
      fig (figure): matplotlib figure object if one wants to re-useit.
      mpi_pool (:class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`): pool of processes
    """
    if distribution is None and data is None:
        raise ValueError("Either distribution or data need to be provided")

    if vartitles is not None and len(vartitles) != distribution.dim:
        raise ValueError("You need to provide the right number of titles.")
    
    if not PLOT_SUPPORT:
        raise RuntimeError("Plotting is not suported")

    if data is None:
        data = computeAlignedConditionals(
            distribution, dimensions_vec=dimensions_vec, pointEval=pointEval,
            range_vec=range_vec, numPointsXax=numPointsXax,
            mpi_pool=mpi_pool)
    nplots = data.nplots
    X_list = data.X_list
    Y_list = data.Y_list
    pdfEval_list = data.pdfEval_list
        
    if fig is None:
        fig = plt.figure(figsize=(8,8));
    else:
        plt.figure(fig.number);
        fig.clf();
    axarr = np.empty((nplots,nplots), dtype=object)
    for i in range(nplots):
        for j in range(1,nplots+1):
            if i == 0 and j == 1:
                axarr[0,0] = plt.subplot( nplots, nplots, (i*nplots)+j);
            else:
                axarr[i,j-1] = plt.subplot( nplots, nplots, (i*nplots)+j,
                                            sharex=axarr[i-1,j-1]);

    if show_title:
        fig.suptitle(title,fontsize=16);
    plt.set_cmap( 'jet' ); #Set colormap
    #plt.subplots_adjust(wspace=.15) #Reduce horizontal distance between subplots
    colorboxes = 'black'
    lw_spines = .5

    # Plot
    idx = 0
    for ii in range(nplots):
        for jj in range(ii+1):
            if jj<ii: # 2d plot
                X = X_list[idx]
                Y = Y_list[idx]
                pdfEval = pdfEval_list[idx]
                #Reshape results for plotting
                pdfEval_mat = pdfEval.reshape( X.shape[0], X.shape[1] )
                #Set current axes
                ax = axarr[ii,jj]
                cont_h = ax.contourf(X, Y, pdfEval_mat, numCont);
                cmin, cmax = cont_h.get_clim();
                cmin = cont_h.levels[1]
                cont_h.cmap.set_under('white');  #Set color below levels
                cont_h.set_clim(cmin, cmax);
                ax.spines['top'].set_color(colorboxes);
                ax.spines['right'].set_color(colorboxes);
                ax.spines['left'].set_color(colorboxes);
                ax.spines['bottom'].set_color(colorboxes);
                ax.spines['top'].set_linewidth(lw_spines);
                ax.spines['right'].set_linewidth(lw_spines);
                ax.spines['left'].set_linewidth(lw_spines);
                ax.spines['bottom'].set_linewidth(lw_spines);
                ax.get_xaxis().set_visible(False);
                ax.get_yaxis().set_visible(False);
                ax.set_aspect('equal');
                idx += 1
    for jj in range(nplots):  #1D plot
        xlin = X_list[idx]
        pdfEval = pdfEval_list[idx]
        maxPdf = np.max(pdfEval)
        #Set current axes
        if nplots == 1:
            ax = axarr
        else:
            ax = axarr[jj,jj]
        ax.plot( xlin , pdfEval );
        ax.plot( xlin[0] , maxPdf*1.1 , color ='white' );
        ax.get_xaxis().set_visible(False);
        ax.get_yaxis().set_visible(False);
        ax.spines['top'].set_color(colorboxes);
        ax.spines['right'].set_color(colorboxes);
        ax.spines['left'].set_color(colorboxes);
        ax.spines['bottom'].set_color(colorboxes);
        ax.spines['top'].set_linewidth(lw_spines);
        ax.spines['right'].set_linewidth(lw_spines);
        ax.spines['left'].set_linewidth(lw_spines);
        ax.spines['bottom'].set_linewidth(lw_spines);
        if vartitles is not None:
            tit = vartitles[jj]
            ax.set_title(tit);
        idx += 1
    for ii in range(nplots):
        for jj in range(ii+1,nplots):
            axarr[ii,jj].set_visible(False);
    fig.canvas.draw();
    if not figname is None:
        plt.savefig(figname, bbox_inches = 'tight')
    else:
        if show_flag:
            plt.show(False);
    return fig

def plotAlignedSliceMap(tr_map, dimensions_vec=0, pointEval=0,
                        range_vec=[-4,4], numPointsXax = 30, numCont = 30,
                        figname=None, show_flag=True, tickslabelsize = 6,
                        show_title=False, fig=None, mpi_pool=None):
    r""" Plot the conditionals aligned with the axis

    Args:
      tr_map (:class:`TriangularTransportMap`): Triangular transport map
      dimensions_vec (list of int): list of dimensions to be displayed. Default 0: display
        10 dimensions at most.
      pointEval (:class:`ndarray`[:math:`d`]): anchor point. Default is zero.
      range_vec (:class:`list<list>`): range to be displayed. Either a
        :class:`list<list>` [2] of integers, or a :class:`list<list>` [d] of
        :class:`list<list>` [2] of integers.
      numPointsXax (int): number of points for each axis.
      numCont (int): number of contours in the contour plots.
      figname (str): if defined, store the figure in the provided path.
      show_flag (bool): whether to show the plot before returning
      show_title (bool): whether to show a title on top of the figure
      fig (figure): matplotlib figure object if one wants to re-use it.
      mpi_pool (:class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`): pool of processes
    """
    if not PLOT_SUPPORT:
        raise RuntimeError("Plotting is not suported")
    dim = tr_map.dim
    #Assign optional parameters if not defined
    if dimensions_vec == 0:
       dimensions_vec = range( min(dim,10) )
    if pointEval ==0:
       pointEval=np.zeros(dim)

    nplots = len(dimensions_vec) # number of subplots per dimension
    if fig is None:
        fig = plt.figure(figsize=(8,8))
    else:
        plt.figure(fig.number)
        fig.clf()
    axarr = np.empty((nplots,nplots), dtype=object)
    for i in range(nplots):
        for j in range(1,nplots+1):
            if i != 0 or j != 0:
                axarr[i,j-1] = plt.subplot( nplots, nplots, (i*nplots)+j,
                                          sharex=axarr[0,0])
            else:
                axarr[i,j-1] = plt.subplot( nplots, nplots, (i*nplots)+j)

    # Prepare range_vec
    if isinstance(range_vec[0], int):
        range_vec = [range_vec] * tr_map.dim

    if show_title:
        fig.suptitle('Slices map along coordinate axes',fontsize=16)
    #plt.set_cmap( 'jet' ) #Set colormap
    plt.set_cmap( 'Blues' )
    #plt.subplots_adjust(wspace=.15) #Reduce horizontal distance between subplots
    colorboxes = 'black'
    lw_spines = .5

    # Create list of points (for every plot)
    X_list = []
    Y_list = []
    tempMat_list = []
    for ii in range(nplots):
        for jj in range(ii+1):
            if jj<ii: # 2d plot
                #The x variable is jj, whereas the y-variable is ii.
                #Create evaluation grid
                xlin = np.linspace( range_vec[jj][0] , range_vec[jj][1],
                                    num=numPointsXax) + \
                       pointEval[jj] #Notice x -- jj
                ylin = np.linspace( range_vec[ii][0] , range_vec[ii][1],
                                    num=numPointsXax) + \
                       pointEval[ii]
                X, Y = np.meshgrid(xlin, ylin)
                X_eval = X.flat #Flat iterator over the array
                Y_eval = Y.flat
                #Slice 2d pdf
                npointEval =len(X_eval) #Number of points where to evaluate the slice
                tempMat = np.tile(pointEval,(npointEval,1))
                tempMat[:,dimensions_vec[ii]] = Y_eval
                tempMat[:,dimensions_vec[jj]] = X_eval
                X_list.append(X)
                Y_list.append(Y)
                tempMat_list.append(tempMat)

    # Evaluate
    npoints_list = [0] + [ tmat.shape[0] for tmat in tempMat_list ]
    npoints_pos = np.cumsum(npoints_list)
    tempMat_mat = np.concatenate(tempMat_list, axis=0)
    scatter_tuple = (['x'], [tempMat_mat])
    mapEval_mat = mpi_eval("evaluate", obj=tr_map,
                           scatter_tuple=scatter_tuple,
                           mpi_pool=mpi_pool)
    mapEval_list = [ mapEval_mat[npoints_pos[i]:npoints_pos[i+1]]
                     for i in range(len(tempMat_list)) ]

    # Plot
    idx = 0
    for ii in range(nplots):
        for jj in range(ii+1):
            if jj<ii: # 2d plot
                X = X_list[idx]
                Y = Y_list[idx]
                tempMat = tempMat_list[idx]
                mapEval = mapEval_list[idx]
                #Reshape results for plotting
                mapEval_mat = mapEval[:,ii].reshape( X.shape[0], X.shape[1] )
                #Set current axes
                ax = axarr[ii,jj]
                cont_h = ax.contourf(X, Y, mapEval_mat, numCont)
                # cmin, cmax = cont_h.get_clim()
                #cmin = cont_h.levels[1]
                #cont_h.cmap.set_under('white')  #Set color below levels
                #cont_h.set_clim(cmin, cmax+10)
                ax.spines['top'].set_color(colorboxes)
                ax.spines['right'].set_color(colorboxes)
                ax.spines['left'].set_color(colorboxes)
                ax.spines['bottom'].set_color(colorboxes)
                ax.spines['top'].set_linewidth(lw_spines)
                ax.spines['right'].set_linewidth(lw_spines)
                ax.spines['left'].set_linewidth(lw_spines)
                ax.spines['bottom'].set_linewidth(lw_spines)
                ax.get_xaxis().set_visible(False)
                ax.get_yaxis().set_visible(False)
                ax.set_aspect('equal')

    max1dplot = 0
    min1dplot = 0
    for jj in range(nplots):  #1D plot
        xlin = np.linspace( range_vec[jj][0] , range_vec[jj][1],
                            num=numPointsXax) + pointEval[jj]
        #Slice 1d pdf
        npointEval =len(xlin) #Number of points where to evaluate the slice
        tempMat = np.tile(pointEval,(npointEval,1))
        tempMat[:,dimensions_vec[jj]] = xlin
        #Evaluate distribution on the slice
        mapEval = tr_map.evaluate(tempMat)[:,jj]
        max1dplot = max(max1dplot , max(mapEval) )
        min1dplot = min(min1dplot , min(mapEval) )
        #maxPdf = np.max(pdfEval)
        #Set current axes
        if nplots == 1:
            ax = axarr
        else:
            ax = axarr[jj,jj]
        ax.plot( xlin , mapEval )
        #ax.plot( xlin[0] , maxPdf*1.1 , color ='white' )
        ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        ax.yaxis.tick_right()
        ax.yaxis.set_ticks_position('right') # Set the y-ticks to only the right
        ax.tick_params(direction='out')
        ax.tick_params(axis='y', colors=colorboxes, labelsize = tickslabelsize)
        ax.spines['top'].set_color(colorboxes)
        ax.spines['right'].set_color(colorboxes)
        ax.spines['left'].set_color(colorboxes)
        ax.spines['bottom'].set_color(colorboxes)
        ax.spines['top'].set_linewidth(lw_spines)
        ax.spines['right'].set_linewidth(lw_spines)
        ax.spines['left'].set_linewidth(lw_spines)
        ax.spines['bottom'].set_linewidth(lw_spines)
    max1dplot = int( np.ceil(max1dplot*1.1) )
    min1dplot = int ( np.floor(min1dplot*1.1) )
    delta = max1dplot - min1dplot
    quart_delta = delta/4.
    tick_quarter = int(min1dplot+quart_delta)
    tick_triquarter = int(min1dplot+3.*quart_delta)
    for jj in range(nplots):
         if nplots == 1:
           ax = axarr
         else:
           ax = axarr[jj,jj]
         ax.set_ylim([min1dplot, max1dplot])
         plt.setp(ax, yticks=[min1dplot, tick_quarter, 0, tick_triquarter, max1dplot])
    for ii in range(nplots):
        for jj in range(ii+1,nplots):
            axarr[ii,jj].set_visible(False)
    fig.canvas.draw()
    if not figname is None:
        plt.savefig(figname, bbox_inches = 'tight')
    else:
        if show_flag:
            plt.show(False)
    return fig

class RandomConditionalsObject(TM.TMO):
    def __init__(self, nplots, X_list, Y_list, pdfEval_list):
        self.nplots = nplots
        self.X_list = X_list
        self.Y_list = Y_list
        self.pdfEval_list = pdfEval_list
    
def computeRandomConditionals(distribution, num_conditionalsXax=0, pointEval=None,
                              range_vec=[-3,3], numPointsXax = 30, mpi_pool=None):
    r""" Compute the random conditionals

    Args:
      distribution (:class:`Distribution`): distribution :math:`\pi`
      num_conditionalsXax (int): number of random conditionals per axis
      pointEval (:class:`ndarray`[:math:`d`]): anchor point. Default is zero.
      range_vec (:class:`tuple`[2]): range to be displayed.
      numPointsXax (int): number of points for each axis.
      mpi_pool (:class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`): pool of processes
    """
    dim = distribution.dim
    #Assign optional parameters if not defined
    if num_conditionalsXax == 0:
       num_conditionalsXax = 4 # number of subplots per dimension
    if pointEval is None:
       pointEval=np.zeros(dim)
        # Create list of points (for every plot)
    X_list = []
    Y_list = []
    tempMat_list = []
    for ii in range(num_conditionalsXax):
        for jj in range(num_conditionalsXax):
            #The x variable is jj, whereas the y-variable is ii.
            #Create evaluation grid
            xlin = np.linspace( range_vec[0] , range_vec[1], num=numPointsXax)  #Notice x -- jj
            ylin = np.linspace( range_vec[0] , range_vec[1], num=numPointsXax)
            X, Y = np.meshgrid(xlin, ylin)
            X_eval = X.flat #Flat iterator over the array
            Y_eval = Y.flat
            #Generate a pair of random orthogonal directions
            Q_rand  = np.random.randn( dim , 2 )
            Q_rand[:,0] = Q_rand[:,0]/np.linalg.norm(Q_rand[:,0])
            Q_rand[:,1] = Q_rand[:,1] - np.dot( Q_rand[:,0], Q_rand[:,1])*Q_rand[:,0]
            Q_rand[:,1] = Q_rand[:,1]/np.linalg.norm(Q_rand[:,1])
            #Slice 2d pdf
            tempMat = np.dot( np.vstack((X_eval, Y_eval)).T, Q_rand.T )
            tempMat += pointEval
            # Append
            X_list.append(X)
            Y_list.append(Y)
            tempMat_list.append(tempMat)

    # Evaluate
    npoints_list = [0] + [ tmat.shape[0] for tmat in tempMat_list ]
    npoints_pos = np.cumsum(npoints_list)
    tempMat_mat = np.concatenate(tempMat_list, axis=0)
    scatter_tuple = (['x'], [tempMat_mat])
    pdfEval_mat = mpi_eval("pdf", obj=distribution,
                           scatter_tuple=scatter_tuple,
                           mpi_pool=mpi_pool)
    pdfEval_list = [ pdfEval_mat[npoints_pos[i]:npoints_pos[i+1]]
                     for i in range(len(tempMat_list)) ]

    data = RandomConditionalsObject(num_conditionalsXax,
                                    X_list, Y_list, pdfEval_list)
    return data
    
def plotRandomConditionals(distribution=None, data=None, num_conditionalsXax=0, pointEval=None,
                           range_vec=[-3,3], numPointsXax = 30, numCont = 15,
                           figname=None, show_flag=True, 
                           show_title=False, title="Random conditionals",
                           fig=None,
                           mpi_pool=None):
    r""" Plot the random conditionals

    Args:
      distribution (:class:`Distribution`): distribution :math:`\pi`
      data (:class:`RandomConditionalsObject`): output of :func:`computeRandomConditionals`
      num_conditionalsXax (int): number of random conditionals per axis
      pointEval (:class:`ndarray`[:math:`d`]): anchor point. Default is zero.
      range_vec (:class:`tuple`[2]): range to be displayed.
      numPointsXax (int): number of points for each axis.
      numCont (int): number of contours in the contour plots.
      figname (str): if defined, store the figure in the provided path.
      show_flag (bool): whether to show the plot before returning
      show_title (bool): whether to show the title
      fig (figure): matplotlib figure object if one wants to re-use it.
      mpi_pool (:class:`mpi_map.MPI_Pool<mpi_map.MPI_Pool>`): pool of processes
    """
    if distribution is None and data is None:
        raise ValueError("Either distribution or data need to be provided")
    
    if not PLOT_SUPPORT:
        raise RuntimeError("Plotting is not suported")

    if data is None:
        data = computeAlignedConditionals(
            distribution, dimensions_vec=dimensions_vec,
            num_conditionalsXax=num_conditionalsXax, pointEval=pointEval,
            range_vec=range_vec, numPointsXax=numPointsXax,
            mpi_pool=mpi_pool)
    num_conditionalsXax = data.nplots
    X_list = data.X_list
    Y_list = data.Y_list
    pdfEval_list = data.pdfEval_list
        
    if fig is None:
        fig = plt.figure(figsize=(8,8));
    else:
        plt.figure(fig.number);
        fig.clf()
    axarr = np.empty((num_conditionalsXax,num_conditionalsXax), dtype=object)
    for i in range(num_conditionalsXax):
        for j in range(1,num_conditionalsXax+1):
            if i != 0 or j != 0:
                axarr[i,j-1] = plt.subplot(num_conditionalsXax, num_conditionalsXax,
                                           (i*num_conditionalsXax)+j, sharex=axarr[0,0]);
            else:
                axarr[i,j-1] = plt.subplot(
                    num_conditionalsXax, num_conditionalsXax, (i*num_conditionalsXax)+j);
    if show_title:
        fig.suptitle(title,fontsize=16);
    plt.set_cmap( 'jet' ); #Set colormap
    #plt.subplots_adjust(wspace=.15) #Reduce horizontal distance between subplots
    colorboxes = 'black'
    lw_spines = .5

    # Plot
    idx = 0
    for ii in range(num_conditionalsXax):
        for jj in range(num_conditionalsXax):
            X = X_list[idx]
            Y = Y_list[idx]
            pdfEval = pdfEval_list[idx]
            #Reshape results for plotting
            pdfEval_mat = pdfEval.reshape( X.shape[0], X.shape[1] )
            #Set current axes
            ax = axarr[ii,jj]
            cont_h = ax.contourf(X, Y, pdfEval_mat, numCont);
            cmin, cmax = cont_h.get_clim();
            cmin = cont_h.levels[1]
            cont_h.cmap.set_under('white');  #Set color below levels
            cont_h.set_clim(cmin, cmax);
            ax.spines['top'].set_color(colorboxes);
            ax.spines['right'].set_color(colorboxes);
            ax.spines['left'].set_color(colorboxes);
            ax.spines['bottom'].set_color(colorboxes);
            ax.spines['top'].set_linewidth(lw_spines);
            ax.spines['right'].set_linewidth(lw_spines);
            ax.spines['left'].set_linewidth(lw_spines);
            ax.spines['bottom'].set_linewidth(lw_spines);
            ax.get_xaxis().set_visible(False);
            ax.get_yaxis().set_visible(False);
            ax.set_aspect('equal');
            idx += 1
    fig.canvas.draw();
    if not figname is None:
        plt.savefig(figname, bbox_inches = 'tight');
    else:
        if show_flag:
            plt.show(False);
    return fig

# def niceBoxplot(data, box_loc=0, widhts_val = .5,
#                 xlabel="", ylabel="", title="",
#                 xtickslabel = 0, logyscale = 0):
#     if not PLOT_SUPPORT:
#         raise RuntimeError("Plotting is not suported")
#     nboxes = data.shape[1]
#     #Assign unassigned optional arguments
#     if box_loc == 0:
#        box_loc = np.linspace(1,3*nboxes,nboxes)

#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     beta = .25
#     bplot = ax.boxplot( data, notch=False, positions = box_loc,
#                         widths = widhts_val, patch_artist=True,
#                         showmeans=False, showfliers=False)
#     ax.set_xlabel(xlabel)
#     ax.set_ylabel(ylabel)
#     ax.set_title(title)
#     ax.set_xlim(-1, max(box_loc)+2)
#     if logyscale==1:
#        ax.set_yscale('log')
#     if xtickslabel != 0:
#        ax.set_xticklabels( [ "$%d\\times10^{%d}$"%frexp10( xtickslabel[ii] ) for  ii in  range(len(box_loc)) ] ) #List comprehension
#     ylab = ax.get_yticklabels()
#     def mjrFormatter(x, pos):
#       return "$%.1f\\times10^{%d}$"%frexp10(x,numdecimals=2)
#     ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(mjrFormatter))
#     for patch in bplot['boxes']:
#         patch.set_facecolor('lightblue')
#         patch.set_edgecolor('darkblue')
#         patch.set_alpha(.5)
#     plt.setp(bplot['whiskers'],linestyle = '-',color='darkblue',alpha=.5)
#     plt.setp(bplot['caps'],color='darkblue',alpha=.5)
#     coloraxes = 'gray'
#     ax.spines['right'].set_visible(False) # Remove the right axis boundary
#     ax.spines['top'].set_visible(False)  # Remove the top axis boundary
#     ax.xaxis.set_ticks_position('bottom') # Set the x-ticks to only the bottom
#     ax.yaxis.set_ticks_position('left') # Set the y-ticks to only the left
#     ax.spines['bottom'].set_position(('axes',-0.04)) # Offset the bottom scale from the axis
#     ax.spines['left'].set_position(('axes',-0.04))  # Offset the left scale from the axis
#     ax.spines['left'].set_linewidth(.5)
#     ax.spines['bottom'].set_linewidth(.5)
#     ax.spines['bottom'].set_color(coloraxes)
#     ax.spines['left'].set_color(coloraxes)
#     ax.xaxis.label.set_color(coloraxes)
#     ax.yaxis.label.set_color(coloraxes)
#     ax.tick_params(axis='x', colors=coloraxes)
#     ax.tick_params(axis='y', colors=coloraxes)
#     ax.yaxis.label.set_size(18)
#     ax.xaxis.label.set_size(18)
#     ax.title.set_color(coloraxes)
#     ax.title.set_size(16)
#     return fig

# def accuracyIntegratedExponentialDiagnostic( distribution1, distribution2,
#                                              numMCsamples = 1e4,
#                                              order_increase = 2,
#                                              figname=None, show_flag=True ):
#     r""" Variance diagnositc

#     Statistical analysis of the variance diagnostic

#     .. math::

#        \mathcal{D}_{KL}(\pi_1 \Vert \pi_2) \approx \frac{1}{2} \mathbb{V}_{\pi_1} \left( \log \frac{\pi_1}{\pi_2}\right)

#     Args:
#       distribution1 (:class:`DIST.Distribution`): distribution :math:`\pi_1`, with which one must be able to approximate
#         integrals (i.e. must be able to sample from :math:`\pi_1`)
#       distribution2 (:class:`DIST.Distribution`): distribution :math:`\pi_2`
#       numMCsamples (int): number of samples
#       order_increase (int): number of increases of the order for the
#         integral approximation.
#       figname (str): if defined, store the figure in the provided path.
#       show_flag (bool): whether to show the plot before returning
#     """
#     if not PLOT_SUPPORT:
#         raise RuntimeError("Plotting is not suported")
#     d2 = copy.deepcopy(distribution2)
#     tm = d2.transport_map
#     if not isinstance(tm, MAPS.IntegratedExponentialTriangularTransportMap):
#         raise ValueError("The transport map must be of type " +
#                          "IntegratedExponentialTriangularTransportMap")
#     base_ord_list = [ t.integ_ord_mult for t in tm.approx_list ]

#     dim = distribution1.dim
#     #Will compute the variance diagnostic for an increasing number of samples
#     allVar = np.zeros( order_increase + 1 )
#     samplesMat =distribution1.rvs( int( numMCsamples ) )
#     for ii in range(order_increase+1):
#         logger.info("accuracyIntegratedExponentialDiagnostic: Iteration %d" % ii)
#         for t,bo in zip(tm.approx_list, base_ord_list):
#             t.integ_ord_mult = bo + ii
#         intEval = distribution1.log_pdf(samplesMat)-d2.log_pdf(samplesMat)
#         allVar[ii] = np.var( intEval )
#     allVar = allVar/2.
#     #fig = plt.semilogy(range(order_increase+1), allVar)
#     fig = nicePlot( range(order_increase+1), allVar ,  logyscale=True , title="Accuracy integrated exponential", xlabel="Integration order", ylabel="Variance diagnostic" )
#     if not figname is None:
#         fig.savefig(figname, bbox_inches = 'tight' )
#     else:
#         if show_flag:
#             plt.show(False)

# def nicePlot( x , y, xlabel="", ylabel="", title="", xtickslabel = 0,
#               linewidth=2, logyscale = False, logxscale = False, linestyle='b',
#               figname=None, show_flag=True):
#     if not PLOT_SUPPORT:
#         raise RuntimeError("Plotting is not suported")
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     if logyscale and logxscale:
#        plot1 = ax.loglog( x, y, linestyle )
#     elif  logyscale:
#        plot1 = ax.semilogy( x, y, linestyle )
#     elif  logxscale:
#        plot1 = ax.semilogx( x, y, linestyle )
#     else:
#        plot1 = ax.plot( x, y, linestyle )

#     plt.setp(plot1, linewidth=linewidth)
#     ax.set_xlabel(xlabel)
#     ax.set_ylabel(ylabel)
#     ax.set_title(title)

#     coloraxes = 'gray'
#     ax.spines['right'].set_visible(False) # Remove the right axis boundary
#     ax.spines['top'].set_visible(False)  # Remove the top axis boundary
#     ax.xaxis.set_ticks_position('bottom') # Set the x-ticks to only the bottom
#     ax.yaxis.set_ticks_position('left') # Set the y-ticks to only the left
#     ax.spines['bottom'].set_position(('axes',-0.04)) # Offset the bottom scale from the axis
#     ax.spines['left'].set_position(('axes',-0.04))  # Offset the left scale from the axis
#     ax.spines['left'].set_linewidth(.5)
#     ax.spines['bottom'].set_linewidth(.5)
#     ax.spines['bottom'].set_color(coloraxes)
#     ax.spines['left'].set_color(coloraxes)
#     ax.xaxis.label.set_color(coloraxes)
#     ax.yaxis.label.set_color(coloraxes)
#     ax.tick_params(axis='x', colors=coloraxes)
#     ax.tick_params(axis='y', colors=coloraxes)
#     ax.yaxis.label.set_size(18)
#     ax.xaxis.label.set_size(18)
#     ax.title.set_color(coloraxes)
#     ax.title.set_size(16)
#     fig.subplots_adjust(bottom=0.14)
#     if not figname is None:
#         fig.savefig(figname, bbox_inches = 'tight' )
#     else:
#         if show_flag:
#             plt.show(False)

#     return fig

# def niceContour( x , y, z, xlabel="", ylabel="", title="",
#                  numCont = 30, xlim=[-3,3], ylim=[-3,3],
#                  colormap='Blues', contourf = False, colorbar=False,
#                  figname=None, show_flag=True):
#     if not PLOT_SUPPORT:
#         raise RuntimeError("Plotting is not suported")
#     plt.set_cmap( colormap )
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     if contourf:
#         cont = ax.contourf(x, y, z, numCont)
#     else:
#         cont = ax.contour(x, y, z, numCont)
#     coloraxes = 'gray'
#     #Set axis limits
#     ax.set_ylim(ylim[0],ylim[1])
#     ax.set_xlim(xlim[0],xlim[1])
#     #Remove last level
#     cmin, cmax = cont.get_clim()
#     cont.cmap.set_under('white')  #Set color below level
#     cmin = cont.levels[1]
#     cont.set_clim(cmin, cmax)  #Set limit levels
#     plt.draw()
#     #Colorbar
#     if colorbar:
#         cbar = plt.colorbar(cont)
#         prop = plt.getp(cbar.ax.axes, 'yticklabels')
#         plt.setp(prop, color=coloraxes)
#         cbar.outline.set_edgecolor(coloraxes)
#         cbar.ax.tick_params(color=coloraxes)
#     #Assign labels and title
#     ax.set_xlabel(xlabel)
#     ax.set_ylabel(ylabel)
#     ax.set_title(title)
#     #Axis aspect
#     ax.spines['right'].set_visible(False) # Remove the right axis boundary
#     ax.spines['top'].set_visible(False)  # Remove the top axis boundary
#     ax.xaxis.set_ticks_position('bottom') # Set the x-ticks to only the bottom
#     ax.yaxis.set_ticks_position('left') # Set the y-ticks to only the left
#     ax.spines['bottom'].set_position(('axes',-0.04)) # Offset the bottom scale from the axis
#     ax.spines['left'].set_position(('axes',-0.04))  # Offset the left scale from the axis
#     ax.spines['left'].set_linewidth(.5)
#     ax.spines['bottom'].set_linewidth(.5)
#     ax.spines['bottom'].set_color(coloraxes)
#     ax.spines['left'].set_color(coloraxes)
#     ax.xaxis.label.set_color(coloraxes)
#     ax.yaxis.label.set_color(coloraxes)
#     ax.tick_params(axis='x', colors=coloraxes)
#     ax.tick_params(axis='y', colors=coloraxes)
#     ax.yaxis.label.set_size(18)
#     ax.xaxis.label.set_size(18)
#     ax.title.set_color(coloraxes)
#     ax.title.set_size(16)
#     fig.subplots_adjust(bottom=0.14)
#     ax.set_aspect('equal')
#     if not figname is None:
#         fig.savefig(figname, bbox_inches = 'tight' )
#     else:
#         if show_flag:
#             plt.show(False)

#     return fig

# def plot2distribution( distribution, xlabel="", ylabel="", title="",
#                   numCont = 30, xlim=[-3,3], ylim=[-3,3], numPointsXax = 150,
#                   colormap='Blues', contourf = False, colorbar = False,
#                   figname=None, show_flag=True):
#     if not PLOT_SUPPORT:
#         raise RuntimeError("Plotting is not suported")
#     #Create evaluation grid
#     xlin = np.linspace( xlim[0] , xlim[1], num=numPointsXax)
#     ylin = np.linspace( ylim[0] , ylim[1], num=numPointsXax)
#     X, Y = np.meshgrid(xlin, ylin)
#     X_eval = X.flatten() #Flat iterator over the array
#     Y_eval = Y.flatten()
#     npointEval =len(X_eval) #Number of points where to evaluate the distribution
#     tempMat = np.vstack( ( X_eval , Y_eval  ) )
#     tempMat = tempMat.transpose()
#     #Evaluate the distribution
#     pdfEval = distribution.pdf(tempMat)
#     #Reshape results for plotting
#     pdfEval_mat = pdfEval.reshape( X.shape[0], X.shape[1] )
#     niceContour( X , Y, pdfEval_mat, xlabel=xlabel, ylabel=ylabel,
#                  title=title, numCont = numCont, xlim=xlim, ylim=ylim,
#                  colormap=colormap, contourf = contourf, colorbar=colorbar,
#                  figname=figname, show_flag=show_flag)

def plotAlignedMarginals(mat_points, dimensions_vec=0, 
                         white_background=True, do_diag=True, numCont=15,
                         show_axis=True, show_title=False,
                         figname=None, show_flag=True, 
                         title='Marginals along coordinate axes',
                         fig=None):
    r""" Plot the marginals aligned with the axis

    Args:
      mat_points (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): samples
      dimensions_vec (list of int): list of dimensions to be displayed. Default 0: display
        10 dimensions at most.
      white_background (bool): whether to have a white background of to use the last
        layer of the colormap
      do_diag (bool): whether to include the one dimensional marginals on the diagonal
      numCont (int): number of contours in the contour plots.
      show_axis (bool): whether to show the axis
      figname (str): if defined, store the figure in the provided path.
      show_flag (bool): whether to show the plot before returning
      fig (figure): matplotlib figure object if one wants to re-use it.
    """
    if not PLOT_SUPPORT:
        raise RuntimeError("Plotting is not suported")
    dim = mat_points.shape[1]
    #Assign optional parameters if not defined
    if dimensions_vec == 0:
        dimensions_vec = list(range( min(dim,20) ))
    else:
        dimensions_vec = list(dimensions_vec)
    if (np.max(dimensions_vec)+1)>dim:
        raise RuntimeError("Desired dimensions not available")

    if fig is None:
        fig = plt.figure(figsize=(8,8));
    else:
        plt.figure(fig.number);
        fig.clf();
    
    nplots = len(dimensions_vec) # number of subplots per dimension
    naxes = nplots if do_diag else nplots - 1
    axarr = np.empty((naxes,naxes), dtype=object)
    for i in range(naxes):
        for j in range(1,naxes+1):
            if i == 0 and j == 1:
                axarr[0,0] = plt.subplot( naxes, naxes, (i*naxes)+j );
            else:
                axarr[i,j-1] = plt.subplot( naxes, naxes, (i*naxes)+j,
                                            sharex=axarr[i-1,j-1] );

    if show_title:
        fig.suptitle(title,fontsize=16);
    plt.set_cmap( 'jet' ); #Set colormap
    # plt.subplots_adjust(wspace=.15) #Reduce horizontal distance between subplots
    colorboxes = 'black'
    lw_spines = .5

    # Plot
    idx = 0
    for ii in range(nplots):
        for jj in range(ii+1):
            if jj<ii: # 2d plot
                index_xx = dimensions_vec[jj]
                index_yy = dimensions_vec[ii]
                xx = mat_points[:,index_xx]
                yy = mat_points[:,index_yy]

                xx_min = xx.min()
                xx_max = xx.max()
                yy_min = yy.min()
                yy_max = yy.max()

                XX, YY = np.mgrid[xx_min:xx_max:100j, yy_min:yy_max:100j]
                positions = np.vstack([XX.ravel(), YY.ravel()])
                values = np.vstack([xx, yy])
                kernel = scistat.gaussian_kde(values)

                ZZ = np.reshape(kernel(positions).T, XX.shape)

                if do_diag:
                    ax = axarr[ii,jj]
                else:
                    ax = axarr[ii-1, jj]

                cont_h = ax.contourf(XX,YY,ZZ, numCont);
                if white_background:
                    cmin, cmax = cont_h.get_clim();
                    cmin = cont_h.levels[1]
                    cont_h.cmap.set_under('white');  #Set color below levels
                    cont_h.set_clim(cmin, cmax);

                ax.set_xlim([xx_min, xx_max]);
                ax.set_ylim([yy_min, yy_max]);

                ax.spines['top'].set_color(colorboxes);
                ax.spines['right'].set_color(colorboxes);
                ax.spines['left'].set_color(colorboxes);
                ax.spines['bottom'].set_color(colorboxes);
                ax.spines['top'].set_linewidth(lw_spines);
                ax.spines['right'].set_linewidth(lw_spines);
                ax.spines['left'].set_linewidth(lw_spines);
                ax.spines['bottom'].set_linewidth(lw_spines);
                ax.get_xaxis().set_visible(ii==(nplots-1) and show_axis);
                ax.get_yaxis().set_visible(jj==0 and show_axis);
                ax.set_aspect('equal');

    if do_diag:
        for jj in range(nplots):  #1D plot
             index_xx = dimensions_vec[jj]
             xx = mat_points[:,index_xx]
             xx_min = xx.min()
             xx_max = xx.max()
             XX = np.linspace(xx_min, xx_max,100)
             kernel = scistat.gaussian_kde(xx)
             pdfEval = kernel.pdf(XX)
             maxPdf = np.max(pdfEval)
             #Set current axes
             if nplots == 1:
               ax = axarr
             else:
               ax = axarr[jj,jj]
             ax.plot( XX , pdfEval );
             ax.plot( XX[0] , maxPdf*1.1 , color ='white' );
             ax.set_xlim([xx_min, xx_max]);
             ax.spines['top'].set_color(colorboxes);
             ax.spines['right'].set_color(colorboxes);
             ax.spines['left'].set_color(colorboxes);
             ax.spines['bottom'].set_color(colorboxes);
             ax.spines['top'].set_linewidth(lw_spines);
             ax.spines['right'].set_linewidth(lw_spines);
             ax.spines['left'].set_linewidth(lw_spines);
             ax.spines['bottom'].set_linewidth(lw_spines);
             ax.get_xaxis().set_visible(jj==(nplots-1) and show_axis);
             ax.get_yaxis().set_visible(False);

    for ii in range(naxes):
        for jj in range(ii+1,naxes):
            axarr[ii,jj].set_visible(False);
    fig.canvas.draw();
    if not figname is None:
        plt.savefig(figname, bbox_inches = 'tight');
    else:
        if show_flag:
            plt.show(False);
    return fig

def plotGradXMap(tmap, base_distribution = None, nsamples = 1000,
                 title = "Intensity coefficients map",
                 cmap='Blues', mpi_pool=None, show_flag=True):
    dim = tmap.dim
    if base_distribution == None:
        base_distribution = DIST.StandardNormalDistribution(dim)
    X = base_distribution.rvs(nsamples)
    #Parallel evaluation
    scatter_tuple = (['x'], [X])
    gradient_map = mpi_eval("grad_x", obj=tmap,
                            scatter_tuple=scatter_tuple,
                            mpi_pool=mpi_pool)

    intensityCoeff = np.sum( np.abs( gradient_map),axis = 0)/nsamples
    intensityCoeff_normalized = intensityCoeff / np.max(intensityCoeff)
    return niceSpy(intensityCoeff_normalized, title=title, cmap=cmap, show_flag=show_flag)

def plotLinearityMap(tmap, nlevels=2, threshold=1e-2,
                     title = "Linearity pattern", cmap='Blues', show_flag=True):
    dim = tmap.dim
    lin_mat = np.zeros((dim,dim))
    lvs = np.linspace(0,1,nlevels+1)
    for d, (tm_comp, tm_comp_avar) in enumerate(zip(tmap.approx_list,
                                                    tmap.active_vars)):
        if len(tm_comp.c.multi_idxs) == 0:
            const_midxs_mat = np.zeros((0,len(tm_comp_avar)), dtype=int)
        else:
            const_midxs_mat = np.asarray( tm_comp.c.multi_idxs )
        exp_midxs_mat = np.asarray( tm_comp.h.multi_idxs )
        # Adjust multi-index of the exponential part to map to the linear span approx
        exp_midxs_mat[:,-1] += 1
        # Threshold parameters
        const_threshold_mask = np.abs(tm_comp.c.get_coeffs()) > threshold
        const_midxs_mat = const_midxs_mat[const_threshold_mask,:]
        exp_threshold_mask = np.abs(tm_comp.h.get_coeffs()) > threshold
        exp_midxs_mat = exp_midxs_mat[exp_threshold_mask,:]
        if exp_midxs_mat.shape[0] == 0:
            exp_midxs_mat = np.zeros((1,len(tm_comp_avar)), dtype=int)
            exp_midxs_mat[0,-1] = 1
        # Merge multi-index matrices
        midxs_mat = np.vstack( (const_midxs_mat, exp_midxs_mat) )
        # Compute mixed order
        mixed_ord = np.sum(midxs_mat, axis=1)
        for nl in range(nlevels):
            # Find dimensions of mixed order nl+1 or >=nlevels if nl+1=nlevels
            if nl+1 == nlevels:
                order_idxs = np.where( mixed_ord > nl )[0]
            else:
                order_idxs = np.where( mixed_ord == nl+1 )[0]
            for idx in order_idxs:
                # Find active variables for selected multi-indices
                avar_idxs = np.where( midxs_mat[idx,:] > 0 )[0]
                avar = [tm_comp_avar[i] for i in avar_idxs]
                # Set value on matrix
                lin_mat[d,avar] = lvs[nl+1]
    return niceSpy(lin_mat, title=title, cmap=cmap, show_flag=show_flag, vrange=[0,1])
    
def niceSpy(mat, title = "Intensity coefficients map",
            cmap = 'Blues', show_flag=True, vrange=None):
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ims = ax.imshow(  intensityCoeff,  interpolation='none', title = title )
    plt.set_cmap( cmap )
    if vrange is None:
        vmin = np.min(mat)
        vmax = np.max(mat)
    else:
        vmin = vrange[0]
        vmax = vrange[1]
    ims = ax.matshow(mat, vmin=vmin, vmax=vmax)
    coloraxes = 'gray'
    #Colorbar
    cbar = plt.colorbar(ims)
    prop = plt.getp(cbar.ax.axes, 'yticklabels')
    plt.setp(prop, color=coloraxes)
    cbar.outline.set_edgecolor(coloraxes)
    cbar.ax.tick_params(color=coloraxes)
    #Assign title
    ax.set_title(title)
    #Axis aspect
    ax.spines['left'].set_linewidth(.5)
    ax.spines['bottom'].set_linewidth(.5)
    ax.spines['top'].set_linewidth(.5)
    ax.spines['right'].set_linewidth(.5)
    ax.spines['bottom'].set_color(coloraxes)
    ax.spines['left'].set_color(coloraxes)
    ax.spines['right'].set_color(coloraxes)
    ax.spines['top'].set_color(coloraxes)
    ax.xaxis.label.set_color(coloraxes)
    ax.yaxis.label.set_color(coloraxes)
    ax.tick_params(axis='x', colors=coloraxes)
    ax.tick_params(axis='y', colors=coloraxes)
    ax.yaxis.label.set_size(18)
    ax.xaxis.label.set_size(18)
    ax.title.set_color(coloraxes)
    ax.title.set_size(16)
    ax.set_aspect('equal')
    if show_flag:
        plt.show(False)
    return fig


