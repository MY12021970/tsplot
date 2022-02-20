function hLines = tsplot(ts, addDotsAtSegmentStart, timeTolMultiplier, hAxes)
% TSPLOT Plots a piecewise continuous timeseries as a series of continuous
% segments.
% 
% Usage:
%   hLines = tsplot(ts, addDotsAtSegmentStart, timeTolMultiplier, hAxes)
% 
% Required Inputs:
%   ts - The timeseries to plot
%
% Optional Inputs:
%   addDotsAtSegementStart - Logical value indicating if a dot should be
%       added at the start of a segment. Default is true.
%
%   timeTolMultiplier - Non-negative value that controls how discontinuities
%       are detected in the input timeseries, If the difference in consecutive
%       time points dt[n] = t[n+1] - t[n]
%           dt[n] <= timeTolMultiplier*eps(t[n])
%       is less than the right hand side above, then the 'ts' has a discontinuity
%       in (t[n], t[n+1]). Default value for timeTolMultiplier is 128. Set
%       this to zero to require time points (t[n+1] == t[n]) to exactly
%       repeat to indicate discontinuity.
%
%   hAxes - Handle to a axes to plot the lines. Default creates a new axes.
%       
% Outputs:
%   lineHandles: Array handles to the plotted line objects

% By: Murali Yeddanapudi, 18-Feb-2022

arguments
    ts (1,1) timeseries
    addDotsAtSegmentStart = true
    timeTolMultiplier (1,1) {mustBeNonnegative} = 128
    hAxes (1,1) = gobjects(1)
end

%% Get the time and data values.
% for now only allow timeseries with one signal (TODO)
t = ts.Time;
y = ts.Data;
assert(numel(y) == numel(t));

%% Create or validate the axes to plot into
if isa(hAxes,'matlab.graphics.GraphicsPlaceholder')
    figure, clf(gcf); hAxes = axes;
end
assert(isa(hAxes,'matlab.graphics.axis.Axes'));
hLines = gobjects(0); % empty array to store the line handles

%% Find discontinuities and start indices of continuous segments
% Discontinuty can also be defined as an upper bound on |dy/dt| (TODO)
dt = [nan; diff(t)];
jumpIndices = find(dt <= double(timeTolMultiplier)*eps(t));
segStartIndices = [1; jumpIndices; numel(t)+1];
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

end
