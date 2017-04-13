#|- Funtions List in [.morph]:
#   |- loc
#   |- morph
#      |- loc
#      |- shift, hit_rate in [.basics]
#   |- morph_assim
#      |- morph
#      |- assim in [.assim]
#      |- nonzero_percentile_thres, threshold in [.basics]


import numpy as np
from scipy import ndimage
from scipy.ndimage.filters import uniform_filter
from .basics import shift, hit_rate, nonzero_percentile_thres, threshold
from .assim import assim


def loc(m,U,V):
    # compute delta_loc
    n = len(np.where((abs(m)+abs(U)+abs(V))>0.0001)[0])
    if n == 0:
        Umean = 0
        Vmean = 0
    else:
        Umean = U.reshape(-1).sum()*1./n
        Vmean = V.reshape(-1).sum()*1./n
    return (Umean,Vmean)


def morph(m_rain, a_rain, max_levels=3, min_levels=0, hr_thres=0.5):
    r = 1 #local array radius
    F = np.array([2**i for i in np.arange(max_levels+1)])[::-1][:max_levels+1-min_levels]
    Ny,Nx = a_rain.shape
    m_locx,m_locy = np.meshgrid(np.arange(Nx),np.arange(Ny))
    X,Y = np.meshgrid(np.arange(Nx),np.arange(Ny))
    x,y = np.meshgrid(np.arange(Nx),np.arange(Ny))
    u,v = 0,0
    m_morph = m_rain.copy()
    m_temp = m_rain.copy()
    # Pyramid iteration
    for n in range(len(F)):
        N = F[n]
        #Filter
        m_coarse = m_morph.copy().reshape(Ny/N,N,Nx/N,N).sum(3).sum(1)
        a_coarse = a_rain.copy().reshape(Ny/N,N,Nx/N,N).sum(3).sum(1)
        a_pixel = uniform_filter(a_coarse.copy(), size=3, mode='constant')
        a_pixel[np.where(a_pixel>0.0001)] = 1.
        a_pixel[np.where(a_pixel<0.0001)] = 0.
        a_pixel_res0 = np.repeat(np.repeat(a_pixel,N,axis=0),N,axis=1)
        m_temp[np.where(a_pixel_res0 == 0)] = 0.
        m_morph[np.where(a_pixel_res0 == 0)] = 0.
        for i in range(Ny/N):
            for j in range(Nx/N):
                MOVE = True
                m_local = np.array(m_coarse[max(0,i-r):min(i+r+1,Ny),max(0,j-r):min(j+r+1,Nx)])
                a_local = np.array(a_coarse[max(0,i-r):min(i+r+1,Ny),max(0,j-r):min(j+r+1,Nx)])
                m_local[i-max(0,i-r),j-max(0,j-r)] = 0. #center
                D = np.zeros(m_local.shape)
                # Local hit-rate threshold (Flag:MOVE)
                if m_coarse[i,j] != 0 and N == F[0] and F[0] >= 8:
                    m_local_full = np.array(m_morph[i*N:(i+1)*N,j*N:(j+1)*N])
                    a_local_full = np.array(a_rain[i*N:(i+1)*N,j*N:(j+1)*N])
                    count1 = len(np.where(m_local_full>0)[0])
                    count2 = len(np.where(a_local_full>0)[0])
                    if hit_rate(m_local_full,a_local_full) >= hr_thres or (count1>=0.5*N*N and count2>=0.5*N*N):
                        MOVE = False
                if MOVE:
                    #Morph
                    for k in range(m_local.shape[0]):
                        for l in range(m_local.shape[1]):
                            mask = np.zeros(m_local.shape)
                            mask[k,l] = m_coarse[i,j]
                            D[k,l] = pow(mask+m_local-a_local,2).sum()
                    if D.shape == (3,3):
                        D += np.array([[1.,0,1.],[0,0,0],[1.,0,1.]])
                    if D.min() != D[i-max(0,i-r),j-max(0,j-r)]:
                        m_locy[(i*N<=y)*(y<i*N+N)*(j*N<=x)*(x<j*N+N)] += (np.where(D==D.min())[0][0]-i+max(0,i-r))*N
                        m_locx[(i*N<=y)*(y<i*N+N)*(j*N<=x)*(x<j*N+N)] += (np.where(D==D.min())[1][0]-j+max(0,j-r))*N
                        # change location point by point
                        addv = np.array(m_morph[i*N:(i+1)*N,j*N:(j+1)*N])
                        movex, movey = (np.where(D==D.min())[1][0]-j+max(0,j-r))*N, (np.where(D==D.min())[0][0]-i+max(0,i-r))*N
                        m_morph[i*N+movey:(i+1)*N+movey,j*N+movex:(j+1)*N+movex] += addv
                        m_morph[i*N:(i+1)*N,j*N:(j+1)*N] -= addv
        # store intermediate stage vector fields
        U0 = m_locx-X
        V0 = m_locy-Y
        U0[np.where(m_temp<0.0001)] = 0
        V0[np.where(m_temp<0.0001)] = 0
        u0,v0 = loc(m_temp,U0,V0)
        u += u0
        v += v0
        X = m_locx.copy()
        Y = m_locy.copy()
        m_morph = ndimage.gaussian_filter(m_morph,1)
        m_temp = m_morph.copy()
    return m_morph,u,v

def morph_assim(m_rain, a_rain, max_levels=3, min_levels=0, hr_thres=0.5, percent_thres=99):
    m_copy = threshold(m_rain,thres=nonzero_percentile_thres(m_rain, percent=percent_thres))
    a_copy = threshold(a_rain,thres=nonzero_percentile_thres(a_rain, percent=percent_thres))
    m_copy0 = m_rain.copy()
    a_copy0 = a_rain.copy()
    D0 = assim(m_copy0,a_copy0)
    D = D0
    U,V = 0,0
    #spin-up    
    for k in np.arange(2):
        m_morph,u,v = morph(m_copy,a_copy,max_levels=max_levels,min_levels=min_levels,hr_thres=hr_thres)
        U += round(u)
        V += round(v)
        m_copy = shift(m_copy,round(u),round(v))
    #iteration with ASSIM switch
    for k in np.arange(10):    
        m_morph,u,v = morph(m_copy,a_copy,max_levels=max_levels,min_levels=min_levels,hr_thres=hr_thres)
        U += round(u)
        V += round(v)
        Dp = assim(shift(m_copy0,U,V),a_copy0)
        if Dp > D:
            D = Dp
            m_copy = shift(m_copy,round(u),round(v))
        else:
            U -= round(u)
            V -= round(v)
            break
    return shift(m_copy0,U,V),U,V
 






