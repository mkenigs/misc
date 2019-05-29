#!/usr/bin/env python
"""
Gauge for matplotlib
Modified from http://nbviewer.ipython.org/gist/nicolasfauchereau/794df533eca594565ab3, https://github.com/martindurant/misc/blob/master/gauge.py
Added set() so can be updated dynamically
"""

from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Wedge
import math

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

    def valToDeg(self, value):
        return self.angleStart+value/float(self.valEnd-self.valStart)*(self.angleEnd-self.angleStart)

    def updatedArrow(self):
        theta = self.valToDeg(self.value)
        return self.ax.arrow(*self.center, self.arrowLength * math.cos(math.radians(theta)), self.arrowLength * math.sin(math.radians(theta)), width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')

    def __init__(self, valStart, valEnd, value, colors='hot', title=None, nWedges=30, angleStart=180, angleEnd=0, tickStep=None):

        # Only need to keep values used by set()
        self.value = value
        self.angleStart = angleStart
        self.angleEnd = angleEnd
        self.valStart = valStart
        self.valEnd = valEnd

        # Constants
        radius = 1
        width = .4
        labelPad = .06
        self.center = (0, 0)
        self.arrowLength = .37

        self.fig, self.ax = plt.subplots()

        # Wedges
        # if colors is a colormap
        cmap = cm.get_cmap(colors, nWedges)  # could throw
        wedges = []
        for i in range(nWedges):
            theta0 = self.angleStart+i/float(nWedges)*(self.angleEnd-self.angleStart)
            theta1 = self.angleStart+(i+1)/float(nWedges)*(self.angleEnd-self.angleStart)
            # always want smaller theta first
            if theta1 < theta0:
                theta0, theta1 = theta1, theta0

            wedges.append(Wedge(self.center, radius, theta0, theta1,
                                width=width, facecolor=cmap(i), edgecolor=cmap(i)))

        [self.ax.add_patch(p) for p in wedges]

        # Labels
        if tickStep:
            numTicks = 1 + \
                math.floor((self.valEnd-self.valStart)/float(tickStep))
            for i in range(numTicks):

                theta = self.angleStart+i*tickStep * \
                    (self.angleEnd-self.angleStart)/(self.valEnd-self.valStart)

                x = (radius+labelPad)*math.cos(math.radians(theta))
                y = (radius+labelPad)*math.sin(math.radians(theta))
                text = self.valStart+i*tickStep
                self.ax.text(x, y, text, ha='center', va='center',
                             fontsize=14, fontweight='bold', rotation=theta-90)  # rotate text -90 so baseline faces the gauge

        # Title
        if title:
            self.ax.text(0, -0.14, title, horizontalalignment='center',
                         verticalalignment='center', fontsize=22, fontweight='bold')

        # Arrow
        self.arrow = self.updatedArrow()
        self.ax.add_patch(Circle(self.center, radius=0.02, facecolor='k'))
        self.ax.add_patch(
            Circle(self.center, radius=0.01, facecolor='w', zorder=11))

        # Hide axes
        self.ax.set_frame_on(False)
        self.ax.axes.set_xticks([])
        self.ax.axes.set_yticks([])

        # makes scaling square
        self.ax.axis('equal')

    def set(self, value):
        self.value = value
        self.arrow.remove()
        self.arrow = self.updatedArrow()
