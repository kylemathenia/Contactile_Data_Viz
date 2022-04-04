#!/usr/bin/env python3
"""Goes through all bag files in bag folder, converts to csv's, and creates vizualizations. If the bag files have
already been processed, skips that step."""

# Libs
import os
import multiprocessing

# Locals
from sensor_data import SensorData
from process_bag import ProcessBag
import visualizations as viz


def main(destination_dir_name = 'test_data', topic_list = ['/hub_0/sensor_0','/hub_0/sensor_1']):
    csv_dir_path = os.getcwd() + '\\' + 'processed_data' + '\\' + destination_dir_name
    _ = ProcessBag(destination_dir_name = destination_dir_name, topic_list = topic_list)

    make_viz_for_all(csv_dir_path)

def make_viz_for_all(csv_dir_path):
    data = SensorData()
    for sample_folder in os.listdir(csv_dir_path):
        sample_folder_path = csv_dir_path + '\\' + sample_folder
        os.chdir(sample_folder_path)
        data.prepare_data(csv_data_path=sample_folder_path)
        make_visualizations(data)

def make_visualizations(data):
    # quiver = viz.QuiverAnimation(data.tactile_sensor_0_data['quiver_frames'], filename="quiver_animation_sensor_0", hz=500, save=True)
    # quiver.run()
    # quiver = viz.QuiverAnimation(data.tactile_sensor_1_data['quiver_frames'], filename="quiver_animation_sensor_1", hz=500, save=True)
    # quiver.run()
    quiver_hm = viz.QuiverHeatmapAnimation(data.tactile_sensor_0_data['quiver_frames'], max_force = 7, filename="quiver_heatmap_animation__sensor_0", hz=500, save=True)
    # quiver_hm.run()
    quiver_hm2 = viz.QuiverHeatmapAnimation(data.tactile_sensor_1_data['quiver_frames'], max_force = 7, filename="quiver_heatmap_animation__sensor_1", hz=500, save=True)
    # quiver_hm2.run()
    # heatmap = viz.HeatmapAnimation(data.tactile_sensor_0_data['heatmap_frames'],max_force = 10,filename="heatmap_animation",hz=500,save=False)
    # heatmap.run()

    p1 = multiprocessing.Process(target=quiver_hm.run)
    p1.start()
    p2 = multiprocessing.Process(target=quiver_hm2.run)
    p2.start()
    p1.join()
    p2.join()

if __name__ == "__main__":
    main(destination_dir_name = 'test_data', topic_list = ['/hub_0/sensor_0','/hub_0/sensor_1'])



