# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 2022

@author: Murali Yeddanapudi
"""

def tsplot(t, y, addDotsAtSegmentStart=True, timeTolMultiplier=128):
    """
    Plots a piecewise continuous timeseries.

    Parameters
    ----------
    t : float array (n,) 
        Array of non-decreasing time values
    y : float array (n,)
        An array of signal values 
    addDotsAtSegmentStart : Boolean, optional
        Controls whether to add a dot to indicate the start of continuous inner
        segment. The default is True.
    timeTolMultiplier : Int, optional
        Tolerance multiplier to decided if two consecutive time points are close
        enough to be treated as a point of discontinuity. The default is 128.

    Returns
    -------
    None.

    """
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    # Find indices of the time points where the difference between consecutive
    # time points is less than tolerance. These are points were we consider the
    # time series to be discontinuous.
    # TODO Discontinuity can also be points where |dy/dt| exceeds a threshold.
    dt = np.diff(t,prepend=float('nan'))
    tol = timeTolMultiplier*np.spacing(t)
    disContIdx = np.nonzero(dt <= tol)[0]

    # Draw the continuous segments as solid lines
    tSegs = np.split(t,disContIdx)
    ySegs = np.split(y,disContIdx)
    tySegs = [*sum(zip(tSegs, ySegs),())] # make list of t,y array pairs
    ax.plot(*tySegs, color='#1f77b4')

    # Draw dotted lines across the discontinuous
    tJmps = np.matrix([t[disContIdx-1], t[disContIdx]]).T.tolist()
    yJmps = np.matrix([y[disContIdx-1], y[disContIdx]]).T.tolist()
    tyJmps = [*sum(zip(tJmps, yJmps),())]
    ax.plot(*tyJmps, color='#1f77b4', linestyle=':')
    
    # Add dots to the beginning of the interior segments
    if (addDotsAtSegmentStart):
        ax.scatter(t[disContIdx],y[disContIdx], color='#1f77b4', marker='.')
    
def gents():
    """
    Generates a random piecewise continuous timeseries with about 1000 time
    points between [0,100] and about 10 discontinuities, indicated by
    repeated time values.

    Returns
    -------
    t : float array (n,)
        Array of non-decreasing time values
    y : float array (n,)
        Array of signal values

    """
    import numpy as np
    
    n = 1000 # number of time points
    nb = 10 # number of discontinuities

    tmax = 100.0 # time span is [0, 100]
    t = np.linspace(0,tmax,n)

    # Generate the continuous segments as a sum of 5 sinusoids with random
    # amplitude and frequency.
    nsig = 5
    amin = 0.5
    amax = 1.5
    a = amin + (amax-amin)*np.random.rand(1, nsig) # amplitudes
    pmin = 10
    pmax = 30
    p = pmin + (pmax-pmin)*np.random.rand(nsig, 1) # periods
    f = 2*np.pi*p/tmax # frequencies
    ft = np.matmul(f, t.reshape(1,-1)) # outer product
    y = np.matmul(a, np.sin(ft)).squeeze() # sum of sinusoids

    # Randomly select 'nb' time points to insert discontinuities. Size the
    # discontinuity to be about the same magnitude as the continuous segments
    dIdx = np.cumsum(np.random.randint(0, 2*int(n/nb), nb))
    dIdx = dIdx[dIdx < n].astype(int)

    # Insert additional time points to indicate discontinuities and
    # bump the y values starting at the discontinuities by random amounts
    t = np.insert(t, dIdx, t[dIdx])
    y = np.insert(y, dIdx, y[dIdx])
    dIdx += range(1, 1+len(dIdx))
    yrng = np.max(y) - np.min(y)
    for id in dIdx:
        yb = 2*yrng*np.random.rand(1,1).squeeze() - yrng
        y[id:] += yb

    return t, y

# Main program start here
(t, y) = gents()
tsplot(t, y)