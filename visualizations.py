"""Classes and functions to vizualize the data."""

from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
import numpy as np
import sys


class QuiverAnimation:
    def __init__(self,quiver_frames,filename="quiver",hz=500,save=False):
        self.data=quiver_frames
        self.save = save
        self.filename = filename
        self.hz = hz

    def run(self):
        # 2 dim arrays for x and y. These are the static locations of the arrows on the plot.
        # mgrid takes the format: np.mgrid[x_range_low:x_range_high:num_spots,y_range_low:y_range_high:num_spots]
        X, Y = np.mgrid[:10:3j,:10:3j]
        # U and V are grids where each corresponding spot has x and y values that define the arrows.
        U = self.data[0][0]
        V = self.data[0][1]
        # Single color values for every spot. This would be the z value.
        C = self.data[0][2]

        # Initialize the quiver
        fig, ax = plt.subplots(1,1)
        # C argument can be used for the colors.
        # See all the cmaps at: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        norm = matplotlib.colors.Normalize(vmin=0, vmax=6) # This sets the range for the colors.
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html
        # Q = ax.quiver(X, Y, U, V, C, pivot='mid', units='inches', norm=norm, cmap='plasma')
        Q = ax.quiver(X, Y, U, V, C, pivot='mid', units='inches', norm=norm, cmap='coolwarm',width = .05, scale=1 / 0.5)
        ax.set_xlim(-3, 13)
        ax.set_ylim(-3, 13)

        # You need to set blit=False, or the first set of arrows never gets cleared on subsequent frames.
        # https://matplotlib.org/3.5.1/api/_as_gen/matplotlib.animation.FuncAnimation.html
        if self.save:
            anim = animation.FuncAnimation(fig, self.update_quiver, fargs=(Q,), interval=1000 / self.hz, frames=len(self.data),
                                           blit=False,save_count=sys.maxsize)
            anim.save(self.filename + '.mp4')
        else:
            anim = animation.FuncAnimation(fig, self.update_quiver, fargs=(Q,), interval=1000 / self.hz,
                                           frames=len(self.data),blit=False)
            fig.tight_layout()
            plt.show()

    def update_quiver(self,i, Q):
        """updates the horizontal and vertical vector components by a
        fixed increment on each frame
        """
        U = self.data[i][0]
        V = self.data[i][1]
        C = self.data[i][2]
        Q.set_UVC(U,V,C)
        return Q,



class QuiverHeatmapAnimation:
    def __init__(self,quiver_frames,max_force = 10,filename="quiver_heatmap",hz=500,save=False):
        self.data=quiver_frames
        self.save = save
        self.filename = filename
        self.max_force = max_force
        self.hz = hz

    def run(self):
        fig, ax = plt.subplots(1,1)

        # Heatmap
        self.im = plt.imshow(self.data[0][2], cmap='YlOrRd', interpolation='nearest', animated=True, vmin=0,
                             vmax=self.max_force)

        #Quiver
        # 2 dim arrays for x and y. These are the static locations of the arrows on the plot.
        # mgrid takes the format: np.mgrid[x_range_low:x_range_high:num_spots,y_range_low:y_range_high:num_spots]
        X, Y = np.mgrid[:2:3j,:2:3j]
        # U and V are grids where each corresponding spot has x and y values that define the arrows.
        U = self.data[0][0]
        V = self.data[0][1]
        self.Q = ax.quiver(X, Y, U, V, pivot='mid', units='inches',  color = 'dodgerblue', cmap='YlOrRd',width = .05, scale=1 / 0.5)
        ax.set_xlim(-.5, 2.5)
        ax.set_ylim(-.5, 2.5)

        if self.save:
            anim = animation.FuncAnimation(fig, self.update_quiver, interval=1000 / self.hz, frames=len(self.data),
                                           blit=False,save_count=sys.maxsize)
            anim.save(self.filename + '.mp4')
        else:
            anim = animation.FuncAnimation(fig, self.update_quiver, interval=1000 / self.hz, frames=len(self.data),blit=False)
            plt.show()

    def update_quiver(self,i):
        self.im.set_array((self.data[i][2].transpose()))
        U = self.data[i][0]
        V = self.data[i][1]
        self.Q.set_UVC(U,V)
        return None,



class HeatmapAnimation:
    def __init__(self,frames,max_force = 1,filename="heatmap",hz=500,save=False):
        self.data = frames
        self.max_force = max_force
        self.save = save
        self.filename = filename
        self.hz = hz

    def run(self):
        fig = plt.figure()
        self.im = plt.imshow(self.data[0], cmap='coolwarm', interpolation='nearest',animated=True,vmin=-self.max_force,vmax=self.max_force)
        if self.save:
            anim = animation.FuncAnimation(fig, self.update, frames=len(self.data), interval=1000 / self.hz, blit=True,
                                           save_count=sys.maxsize)
            anim.save(self.filename + '.mp4')
        else:
            anim = animation.FuncAnimation(fig, self.update, frames=len(self.data), interval=1000 / self.hz, blit=True)
        plt.show()

    def update(self,i):
        self.im.set_array((self.data[i]))
        return self.im,
