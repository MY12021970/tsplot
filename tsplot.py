# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 2022

@author: Murali Yeddanapudi
"""
def tsplot(t, y, addDotsAtSegmentStart=True, timeTolMultiplier=128, hAxes):
    
    import numpy
    import numpy.matlib

    # Find discontinuities and start indices of continuous segments
    # Discontinuty can also be defined as an upper bound on |dy/dt| (TODO)
    dt = numpy.diff(t,prepend=float('nan'))
    tol = timeTolMultiplier*numpy.spacing(t)
    jumpIndices = numpy.nonzero(dt <= tol)[0]
    tSegs = numpy.split(t,jumpIndices)
    ySegs = numpy.split(y,jumpIndices)
    
    tJmps = numpy.matrix([t[jumpIndices-1], t[jumpIndices]]).T.tolist()
    yJmps = numpy.matrix([y[jumpIndices-1], y[jumpIndices]]).T.tolist()
    
    
    
    ns = numel(segStartIndices)-1;

    %% Plot the timeseries as a series of sements
    % Draw continuous segments as solid lines and dotted lines across the
    % discontinuities
    for is=1:ns
        startIdx = segStartIndices(is);
        endIdx = segStartIndices(is+1)-1;
        ti = t(startIdx:endIdx);
        yi = y(startIdx:endIdx);
        hLines(end+1) = line(hAxes, ti, yi); %#ok<AGROW>
        
        if endIdx < numel(t)
            tj = [t(endIdx) t(endIdx+1)];
            yj = [y(endIdx) y(endIdx+1)];
            hLines(end+1) = line(hAxes, tj, yj, 'LineStyle', ':'); %#ok<AGROW>
        end
    end

    %% Add dots at the begining of new interior segments
    if addDotsAtSegmentStart
        hLines(end+1) = line(hAxes, t(jumpIndices), y(jumpIndices), ...
            'LineStyle','none', 'Marker','.');
    end