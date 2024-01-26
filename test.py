import numpy as np
from regularAgent import *

def plotResult(point_set, cp):
    plt.clf()
    x_min, x_max = find_x_bounds(point_set)
    interval = Interval(x_min - 10, x_max + 10)
    y_min, y_max = find_y_bounds(point_set)
    prepare_axis(interval.l - 5, interval.r + 5, y_min - 5, y_max + 5)
    plot_point_set(point_set, color='b')
    plot_point(cp, color='r')
    plt.pause(1)
    end = input('Press enter to the next step.')


#pos = [[5,5],[5,5],[5,5],[5,5],[10.254,15.414],[19.391,13.812],[12.166,14.221],[10.29,12.217],[14.379,14.958],[12.331,12.309]]

        
#pos = [[5.667,4.547],[5.667,4.547],[5.667,4.547],[5.667,4.547],[5.667,4.547],[5.667,4.547],[15,15],[15,15],[15,15],[15,15]]
#pos = [[5,5],[5,5],[5,5],[5,5],[5,15],[5,15],[5,15]]
#pos = [[5,5],[5,5],[5,5],[6,5],[6,5],[6,5]]
pos = [[8.159, 12.233],[8.159, 12.233],[8.611, 11.583],[15.456, 5.247]]
point_set = []
for i in pos:
    point_set.append(Point(i[0],i[1]))
cp = Centerpoint()
centerpoint = cp.reduce_then_get_centerpoint(point_set)
plotResult(point_set, centerpoint)
