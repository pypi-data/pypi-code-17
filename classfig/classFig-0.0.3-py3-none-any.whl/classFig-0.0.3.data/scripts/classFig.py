#!python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler # pip install cycler
        
class classFig:
    """
    Class for comfortable figure handling with python / matplotlib   
    @author: fstutzki
    """
    def __init__(self, template='PPT', subplot=(1,1), sharex=False, sharey=False, width=0, height=0, fontfamily='', fontsize=0, linewidth=0, figshow=True):
        """ Set default values and create figure: fig = classFig('OL',(2,2)) """
        self.figshow = figshow # show figure after saving
        self.subplot_geo = subplot # subplot geometry, first value Y-axis (above), second value X-axis (besides)
        self.subplot_cnt = subplot[0]*subplot[1] # number of subplots
        self.axe_current = 0 # current axis
        
        # color
        colorBlue    = np.array([33,101,146])/255 #iap color "blue"
        colorRed     = np.array([218,4,19])/255   #iap color "red"
        colorGreen   = np.array([70,173,52])/255  #iap color "green"
        colorOrange  = np.array([235,149,0])/255  #iap color "orange"
#        colorYellow  = np.array([255,242,0])/255  #iap color "yellow"
#        colorGrey    = np.array([64,64,64])/255   #iap color "black"
        
        if template.lower() == 'ppt':
            tpl_width = 15
            tpl_height = 10
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 2
        elif template.lower() == 'ppttwo':
            tpl_width = 10
            tpl_height = 8
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 2
        elif template.lower() == 'pptbig':
            tpl_width = 20
            tpl_height = 15
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 3
        elif template.lower() == 'ol':
            tpl_width = 8
            tpl_height = 6
            tpl_fontfamily = 'serif'
            tpl_fontsize = 9
            tpl_linewidth = 1
        elif template.lower() == 'oe':
            tpl_width = 12
            tpl_height = 8
            tpl_fontfamily = 'serif'
            tpl_fontsize = 10
            tpl_linewidth = 1
            
        if width==0:
            width = tpl_width
        if height==0:
            height = tpl_height
        if fontfamily=='':
            fontfamily = tpl_fontfamily
        if fontsize==0:
            fontsize = tpl_fontsize
        if linewidth==0:
            linewidth = tpl_linewidth
        
        mpl.rc('font',size=fontsize)
        mpl.rc('font',family=fontfamily)
        mpl.rc('lines',linewidth=linewidth)
        mpl.rc('axes', prop_cycle=(cycler('color', [colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange])+
                                   cycler('linestyle', ['-','-','-','-','--','--','--','--',':',':',':',':','-.','-.','-.','-.'])))
        
        self.figH, self.axeH = plt.subplots(self.subplot_geo[0],self.subplot_geo[1],sharex=sharex,sharey=sharey)
        
        self.figH.set_size_inches(width/2.54,height/2.54)
        
        self.subplot(0)
            
    def subplot(self,iplot=np.NaN):
        """ Set current axis/subplot: fig.subplot(0) for first subplot or fig.subplot() for next subplot """
        if iplot is np.NaN:
            self.axe_current += 1
        else:
            self.axe_current = iplot
        
        self.axe_current = self.axe_current % ( self.subplot_geo[0] * self.subplot_geo[1] )
        if self.subplot_geo == (1,1):
            self.axeC = self.axeH
        elif self.subplot_geo[0] > 1 and self.subplot_geo[1] > 1:
            isuby = self.axe_current // self.subplot_geo[1]
            isubx = self.axe_current % self.subplot_geo[1]
            self.axeC = self.axeH[isuby][isubx]
        else:
            self.axeC = self.axeH[self.axe_current]
        
        return self.axeC
    
    def suptitle(self,*args,**kwargs):
        """ Set super title for the whole figure """
        self.figH.suptitle(*args,**kwargs)
    def plot(self,*args,**kwargs):
        """ Plot data """
        self.axeC.plot(*args,**kwargs)
#        axeC.set_xlim(np.min(x),np.max(x))
    def pcolor(self,*args,**kwargs):
        """ 2D area plot """
        if 'cmap' not in kwargs:
            kwargs['cmap'] = 'nipy_spectral'
        self.axeC.pcolormesh(*args,**kwargs)
    def pcolor_square(self,*args,**kwargs):
        """ 2D area plot with axis equal and off """
        if 'cmap' not in kwargs:
            kwargs['cmap'] = 'nipy_spectral'
        self.axeC.pcolormesh(*args,**kwargs)
        self.axeC.axis('off')
        self.axeC.set_aspect('equal')
    def axis(self,*args,**kwargs):
        """ Access axis properties such as 'off' """
        self.axeC.axis(*args,**kwargs)
    def axis_aspect(self,*args,**kwargs):
        """ Access axis aspect ration """
        self.axeC.set_aspect(*args,**kwargs)
    def title(self,*args,**kwargs):
        """ Set title for current axis """
        self.axeC.set_title(*args,**kwargs)
    def xlabel(self,*args,**kwargs):
        """ Set xlabel for current axis """
        self.axeC.set_xlabel(*args,**kwargs)
    def ylabel(self,*args,**kwargs):
        """ Set ylabel for current axis """
        self.axeC.set_ylabel(*args,**kwargs)
    def xlim(self,xmin=np.inf,xmax=-np.inf):
        """ Set limits for current x-axis: fig.xlim(0,1) or fig.xlim() """
        if np.size(xmin)==2:
            xmax = xmin[1]
            xmin = xmin[0]
        elif xmin==np.inf and xmax==-np.inf:
            for iline in self.axeC.lines:
                x = iline.get_xdata()
                xmin = np.minimum(xmin,np.min(x))
                xmax = np.maximum(xmax,np.max(x))
        self.axeC.set_xlim(xmin,xmax)
    def ylim(self,ymin=np.inf,ymax=-np.inf):
        """ Set limits for current y-axis: fig.ylim(0,1) or fig.ylim() """
        if np.size(ymin)==2:
            ymax = ymin[1]
            ymin = ymin[0]
        elif ymin==np.inf and ymax==-np.inf:
            for iline in self.axeC.lines:
                y = iline.get_ydata()
                ymin = np.minimum(ymin,np.min(y))
                ymax = np.maximum(ymax,np.max(y))
        self.axeC.set_ylim(ymin,ymax)
    def save(self,filename,*args,**kwargs):
        """ Save figure to png, pdf: fig.save('test.png',600,'pdf') """
        dpi = 300
        fileparts = filename.split('.')
        fileformat = set()
        fileformat.add(fileparts[-1])
        filename = filename.replace("."+fileparts[-1],"")
        for attribute in args:
            if isinstance(attribute, int):
                dpi = attribute
            else:
                fileformat.add(attribute)
         
        self.figH.tight_layout()
        #fig.subplots_adjust(hspace=0.1)
        if 'dpi' not in kwargs:
            kwargs['dpi'] = dpi
        for iformat in fileformat:            
            self.figH.savefig(filename+"."+iformat,**kwargs)
        if self.figshow==True:
            plt.show()
            
if __name__ == '__main__':
    fig = classFig('oe',(3,2))
    fig.plot(np.linspace(0,2,10),np.random.rand(10,3)) # plot some data
    fig.subplot() # next subplot
    fig.plot(np.linspace(0,2,10),np.random.rand(10,4))
    fig.xlim() # set limits to min/max values
    fig.title('Random numbers') # set title for current axis
    fig.xlabel('Test')  # set xlabel
    fig.subplot(4) # activate specific subplot
    fig.pcolor(np.random.rand(10,10)) # 2D data plot (uses much fast pcolormesh internally)
    fig.axeC.set_ylabel('Numbers') # all matplotlib functions can be called directly for the current axis
    fig.subplot() # activate specific subplot
    fig.pcolor_square(np.random.rand(10,10)) # 2D data plot with axis off and equal
    fig.save('fig_test.png',600,'pdf') # save figure in multiple format with specified resolution
    