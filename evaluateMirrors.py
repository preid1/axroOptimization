import numpy as np
import matplotlib.pyplot as plt
import scattering as scat
import utilities.imaging.man as man
import axroOptimization.solver as slv
import axroOptimization.conicsolve as conic

import pdb

def correctXrayTestMirror(d,ifs,shade=None,dx=None,azweight=.015,smax=5.,\
                          bounds=None):
    """
    Get distortion on same grid as IFs and run correction.
    Rebin result onto original distortion grid and apply.
    dx should be on IF grid size
    """
    #Rebin to IF grid
    d2 = man.newGridSize(d,np.shape(ifs[0]))

    #Handle shademask
    if shade is None:
        shade = np.ones(np.shape(d2))

    #Run correction
    volt = slv.correctDistortion(d2,ifs,shade,\
                                            dx=dx,azweight=azweight,\
                                            smax=smax,bounds=bounds)
    # Compute the correction on the same scale as the original
    # data. This correction will need to be added to the original
    # data to yield the final corrected figure.
    ifs2 = ifs.transpose(1,2,0)
    cor2 = np.dot(ifs2,volt)
    cor3 = man.newGridSize(cor2,np.shape(d),method='linear')
    #Handle shademask
    cor2[shade==0] = np.nan
    cornan = man.newGridSize(cor2,np.shape(d),method='linear')
    cor3[np.isnan(cornan)] = np.nan

    return cor3,volt

def computeMeritFunctions(d,dx,x0=np.linspace(-2.,2.,1000),\
                          graze=conic.woltparam(220.,8400.)[0],\
                          renorm=True):
    """
    RMS axial slope
    Axial sag
    d in microns
    """
    #Remove NaNs
    d = man.stripnans(d)
        
    #Compute PSF
    primfoc = conic.primfocus(220.,8400.)
    dx2 = x0[1]-x0[0]
    resa = scat.primary2DPSF(d,dx[0],x0=x0)

    #Make sure over 95% of flux falls in detector
    integral = np.sum(resa)*dx2
    if integral < .95:
        print 'Possible sampling problem'
        print str(np.sum(resa)*dx2)

    #Normalize the integral to account for some flux
    #scattered beyond the detector
    if renorm is True:
        resa = resa/integral

    cdf = np.cumsum(resa)*dx2
        
    #Compute PSF merit functions
    # Computing the rms rigorously, but not usefully. 
    #rmsPSF = np.sqrt(np.sum(resa*x0**2)*dx2-(np.sum(resa*x0)*dx2)**2)
    # Computing the rms by assuming a Gaussian profile.
    rmsPSF = x0[np.argmin(np.abs(cdf-.84))]-\
             x0[np.argmin(np.abs(cdf-.16))]
    hpdPSF = x0[np.argmin(np.abs(cdf-.75))]-\
             x0[np.argmin(np.abs(cdf-.25))]
    
    return rmsPSF/primfoc*180/np.pi*60**2*2,hpdPSF/primfoc*180/np.pi*60**2,\
           [x0,resa]
        
def correctHFDFC3(d,ifs,shade=None,dx=None,azweight=.015,smax=5.,\
                          bounds=None):
    """
    Get distortion on same grid as IFs and run correction.
    Rebin result onto original distortion grid and apply.
    dx should be on IF grid size.
    Needs update on doc string!
    """
    #Rebin to IF grid
    d2 = man.newGridSize(d,np.shape(ifs[0]))

    #Handle shademask
    if shade is None:
        shade = np.ones(np.shape(d2))

    #Run correction
    volt = slv.correctDistortion(d2,ifs,shade,\
                                            dx=dx,azweight=azweight,\
                                            smax=smax,bounds=bounds)
    
    #Add correction to original data
    ifs2 = ifs.transpose(1,2,0)
    cor2 = np.dot(ifs2,volt)
    #Handle shademask
    cor2[shade==0] = np.nan
    cor3 = man.newGridSize(cor2,np.shape(d),method='linear')

    return cor3,volt
        
def correctForCTF(d,ifs,shade=None,dx=None,azweight=.015,smax=5.,\
                          bounds=None):
    """
    Get distortion on same grid as IFs and run correction.
    Rebin result onto original distortion grid and apply.
    dx should be on IF grid size.
    Needs update on doc string!
    """
    #Rebin to IF grid
    d2 = man.newGridSize(d,np.shape(ifs[0]))

    #Handle shademask
    if shade is None:
        shade = np.ones(np.shape(d2))

    #Run correction
    volt = slv.correctDistortion(d2,ifs,shade,\
                                            dx=dx,azweight=azweight,\
                                            smax=smax,bounds=bounds)
    # Compute the correction on the same scale as the original
    # data. This correction will need to be added to the original
    # data to yield the final corrected figure.
    ifs2 = ifs.transpose(1,2,0)
    cor2 = np.dot(ifs2,volt)
    #Handle shademask
    cor2[shade==0] = np.nan
    
    return cor2,volt


