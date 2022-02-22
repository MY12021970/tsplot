# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 2022

@author: Murali Yeddanapudi
"""
def gents():
    import numpy
    import numpy.matlib
    
    n = 1001 # number of time points
    nb = 10 # number of discontinuities

    tmax = 100.0 # time span is [0, 100]
    t = numpy.linspace(0,tmax,n)

    # Generate the continuous segments as a sum of 5 sinusoids with random
    # amplitude and frequency.
    nsig = 5
    amin = 0.5
    amax = 1.5
    a = amin + (amax-amin)*numpy.matlib.rand(1, nsig) # amplitudes
    pmin = 10
    pmax = 30
    p = pmin + (pmax-pmin)*numpy.matlib.rand(nsig,1) 
    f = 2*numpy.pi*p/tmax # frequencies
    ft = numpy.matmul(f, t.reshape(1,-1)) # outer product
    y = numpy.matmul(a, numpy.sin(ft)).A1 # sum of sinusoids
    yrng = numpy.max(y) - numpy.min(y)

    # Randomly select 'nb' time points to insert discontinuities. Size the
    # discontinuity to be about the same magnitude as the continuous segments
    bidx = numpy.cumsum(2*numpy.floor((n/nb)*numpy.matlib.rand(1,nb).A1))
    bidx = bidx[bidx < n].astype(int)
 
    t = numpy.insert(t, bidx, t[bidx])
    y = numpy.insert(y, bidx, y[bidx])
    
    bidx += range(1, 1+len(bidx))
    for ib in bidx:
        yb = 2*yrng*numpy.matlib.rand(1).A1 - yrng
        y[ib:] += yb
      
    return t, y
