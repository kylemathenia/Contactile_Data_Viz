#!/usr/bin/env python3
"""
Contactile sensor 0 is the left sensor if you consider the side with the plugs the top.

SensorData class serves as a container for all sensor data in a specified directory that contains ROS topic cvs data
files (produced from bag files). Stores the data in the multiple forms so as to be compatible with different matplotlib
functions.

Each sensor has a dictionary, such as self.tactile_sensor_0_data, which holds the data in different forms.

self.tactile_sensor_0_data['quiver_frames'] contains data for matplotlib quiver plots:
quiver_frames: 1st dim == frame num, 2nd dim == (xforce grid, yforce grid, zforce grid)
Each grid is 2 dim array for which the 1st dim is row, 2nd dim is column of pillars.
Example: self.data[10][1][2][3] is a single force at [11th frame][yforce grid][pillar row 2][pillar column 3]

self.tactile_sensor_0_data['heatmap_frames'] contains data in a form that can create heatmaps for the z force in
matplotlib:
heatmap_frames: 1st dim == frame num, each frame is a 2d grid of z force values for which the 1st dim is row, 2nd dim is
column of pillars.
Example: self.data[10][1][2] is a single force at [11th frame][pillar row 2][pillar column 3]

TODO: Verify pillar positions. Link an image to reference here.
"""

import os
import pandas as pd
import numpy as np

class SensorData:
    def __init__(self):
        # If the filename below is found in the directory, establish the corresponding function to run.
        self.topic_function_bindings = {'hub_0-sensor_0.csv':self.tactile_data,
                                        'hub_0-sensor_1.csv':self.tactile_data}

    def prepare_data(self, csv_data_path = os.getcwd()+'\\'+'processed_data'+'\\'+'test_data'+'\\'+'grasp_release_0degree_0offset_2022-03-27-22-00-10'):
        self.csv_dir = csv_data_path
        self.file_list = self.get_file_names()

        for file_name in self.topic_function_bindings.keys():
            if file_name not in self.file_list:
                self.topic_function_bindings[file_name](file_name,clear_data=True)
            elif file_name in self.file_list:
                dataframe = pd.read_csv(file_name)
                self.topic_data = dataframe.to_numpy()
                self.topic_function_bindings[file_name](file_name,clear_data=False)

    def tactile_data(self,topic,clear_data=False):
        sensor_num = int(topic[len(topic)-5])
        if clear_data and sensor_num == 0:
            self.tactile_sensor_0_data = None
            return
        elif clear_data and sensor_num == 1:
            self.tactile_sensor_1_data = None
            return
        data = {}
        data['quiver_frames'], data['heatmap_frames'] = self.get_tactile_frames()
        if sensor_num == 0: self.tactile_sensor_0_data = data
        else: self.tactile_sensor_1_data = data


    def get_tactile_frames(self):
        """1st dim == frame num, 2nd dim == xforce grid(0), yforce grid(1), zforce grid(2)
        Each grid is 2 dim array. 1st dim is row, 2nd dim is column of pillars."""
        quiver_frames = []
        heatmap_frames = []
        for sample in self.topic_data:
            pillar_data = sample[6]
            pillar_data = pillar_data.strip('[]')
            pillar_data = pillar_data.split(',')
            xgrid, ygrid, zgrid = self.get_xyz_grids(pillar_data)
            quiver_frames.append([xgrid, ygrid, zgrid])
            heatmap_frames.append(zgrid)
        return quiver_frames,heatmap_frames

    def get_xyz_grids(self,pillar_data):
        xgrid = np.empty(0)
        ygrid = np.empty(0)
        zgrid = np.empty(0)
        for i, pillar in enumerate(pillar_data):
            pillar_list = pillar.split('\n')
            fx = pillar_list[10].split(':')
            fx = float(fx[1])
            fy = pillar_list[11].split(':')
            fy = float(fy[1])
            fz = pillar_list[12].split(':')
            fz = float(fz[1])
            xgrid = np.append(xgrid, fx)
            ygrid = np.append(ygrid, fy)
            zgrid = np.append(zgrid, fz)
        xgrid = (np.flip(xgrid)).reshape(3, 3)
        ygrid = (np.flip(ygrid)).reshape(3, 3)
        zgrid = (np.flip(zgrid)).reshape(3, 3)
        return xgrid, ygrid, zgrid

    def get_file_names(self):
        # Change working dir to the right directory in case it got switched.
        os.chdir(self.csv_dir)
        return os.listdir(self.csv_dir)


def main():
    data_inst = SensorData()
    data_inst.prepare_data()
    print(data_inst.tactile_sensor_0_data)

if __name__ == '__main__':
    main()