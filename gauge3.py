#!/usr/bin/env python
"""
Gauge for matplotlib
Modified from http://nbviewer.ipython.org/gist/nicolasfauchereau/794df533eca594565ab3, https://github.com/martindurant/misc/blob/master/gauge.py
Added set() so can be updated dynamically
"""

from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Wedge, Shadow
import math
import numpy as np
from IPython import display


class Gauge():
    """Example usage in Juypter Notebook:

    import time
    from IPython import display
    g=Gauge(0, 100, 0, tickStep=10, title="My Gauge")
    for i in range(6):
        display.display(g.fig)
        g.set(i*20)
        display.clear_output(wait=True)
        time.sleep(.15)
    """

    def __init__(self, valStart, valEnd, value, colors='Wistia', title=None, nWedges=30, angleStart=180, angleEnd=0, tickStep=None):

        # Only need to keep values used by set()
        self.angleStart = angleStart
        self.angleEnd = angleEnd
        self.valStart = valStart
        self.valEnd = valEnd
        self.value = value

        # Constants
        self.radius = 1
        self.width = .45
        self.labelPad = .1
        self.center = (0, 0)
        self.arrowLength = .37

        self.fig, self.ax = plt.subplots()

        # if colors is a colormap
        self.cmap = cm.get_cmap(colors)  # could throw
        self.normalizer = Normalize(vmin=self.valStart, vmax=self.valEnd)

        self.setWedge(self.value)
        self.setText()

        # Background wedge
        (theta0, theta1) = (self.angleStart, self.angleEnd) if self.angleStart < self.angleEnd else (
            self.angleEnd, self.angleStart)
        bgWedge = Wedge(self.center, self.radius, theta0,
                        theta1, width=self.width, facecolor='0.95', edgecolor='k', linewidth=.3)
        self.ax.add_patch(bgWedge)
        self.ax.add_patch(Shadow(bgWedge, .01, -.01))

        # min and max values
        self.ax.text(-self.radius+self.width/2, -self.labelPad,
                     self.valStart, ha='center', va='center', fontsize=14)
        self.ax.text(self.radius-self.width/2, -self.labelPad,
                     self.valEnd, ha='center', va='center', fontsize=14)

        # Title
        if title:
            self.ax.text(0, -self.labelPad, title, horizontalalignment='center',
                         verticalalignment='center', fontsize=10)

        # Hide axes
        self.ax.set_frame_on(False)
        self.ax.axes.set_xticks([])
        self.ax.axes.set_yticks([])

        # makes scaling square
        self.ax.axis('equal')

    def set(self, value):
        if value != self.value:
            oldVal = self.value

            self.value = value

            self.valText.remove()
            self.setText()

            for v in np.arange(oldVal, self.value, (self.value-oldVal)/6):
                self.valWedge.remove()
                self.setWedge(v)
                display.clear_output(wait=True)
                display.display(self.fig)
#                 time.sleep(.0001)
            self.valWedge.remove()
            self.setWedge(self.value)
            display.clear_output(wait=True)
            display.display(self.fig)

    def valToDeg(self, value):
        return self.angleStart+value/float(self.valEnd-self.valStart)*(self.angleEnd-self.angleStart)

    def setText(self):
        self.valText = self.ax.text(0, (self.radius-self.width)/2, '%.2f' % self.value, horizontalalignment='center',
                                    verticalalignment='top', fontsize=28)

    def setWedge(self, value):
        theta0 = self.angleStart
        theta1 = self.valToDeg(value)
        if theta0 > theta1:
            theta0, theta1 = theta1, theta0

        self.valWedge = Wedge(self.center, self.radius, theta0, theta1, width=self.width,
                              facecolor=self.cmap(self.normalizer(value)), edgecolor='k', linewidth=.3)
        self.ax.add_patch(self.valWedge)

class Status:
    def __init__(self, mid, high, value):
        self.mid=mid
        self.high=high
        self.value=value

        self.fig, self.ax = plt.subplots()

        self.drawCircle()
        self.setText()

        # Hide axes
        self.ax.set_frame_on(False)
        self.ax.axes.set_xticks([])
        self.ax.axes.set_yticks([])

        # makes scaling square
        self.ax.axis('equal')

    def drawCircle(self):
        if self.value >= self.high:
            color='r'
        elif self.value>= self.mid:
            color='y'
        else:
            color='g'

        self.indicator = Circle((0,0), radius=1, color=color)
        self.ax.add_patch(self.indicator)

    def setText(self):
        self.valText = self.ax.text(1, 0, '%.2f' % self.value, horizontalalignment='right',
                                    verticalalignment='center',
                                     fontsize=42)

    def set(self, value):
        if value!=self.value:
            self.valText.remove()
            self.indicator.remove()

            self.setText()
            self.drawCircle()
# import time
# import random
# from IPython import display
# g=Gauge(0, 1000, 30, tickStep=100, title="mle_statsmover_executions_total", nWedges=10, colors='Wistia')
# while True:

# #     queryResponse=prom.query('mle_statsmover_executions_total')
# #     newVal=float(queryResponse.json()['data']['result'][1]['value'][1])
#     g.set(random.uniform(.6*g.valEnd, .8*g.valEnd))
# #     display.clear_output(wait=True)
#     time.sleep(.4)