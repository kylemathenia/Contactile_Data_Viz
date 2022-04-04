#!/usr/bin/env python3
"""
Contains the ProcessBag class, which automatically processes bag files into a specified directory name.

Running as __main__ converts all .bag files in a specified source directory to .csv files. Moves csv files to
destination folder within a folder called processed_data.
"""

import shutil
import os
from bagpy import bagreader
import logging

######Params######
destination_directory_name = 'test_data'

class ProcessBag:
    def __init__(self, base_path = os.getcwd(),
                 source_dir_name = 'bag_data',
                 destination_dir_name = 'experiment_files',
                 topic_list = ['/hub_0/sensor_0','/hub_0/sensor_1']):
        self.source_dir = base_path + '\\'+ source_dir_name
        self.destination_dir = base_path + '\\' + 'processed_data' + '\\' + destination_dir_name
        self.topic_list = topic_list
        self.run()

    def run(self):
        if not os.path.exists(self.destination_dir):
            os.makedirs(self.destination_dir)
        # Change working dir to the source directory.
        os.chdir(self.source_dir)
        # For every filename string in the source directory.
        for i, filename in enumerate(os.listdir(self.source_dir)):
            if filename.endswith(".bag"):
                self.convert_to_csv(filename)
            else:
                continue

    def convert_to_csv(self,filename):
        b = bagreader(filename)
        # Save a csv file for each topic in the topic list inside a new folder.
        for topic in self.topic_list:
            name_of_csv_file = b.message_by_topic([topic])
        filename_base = filename.removesuffix('.bag')
        topic_folder_path = self.source_dir + '\\' + filename_base
        # Move the folder to a the destination folder.
        try:
            _ = shutil.move(topic_folder_path, self.destination_dir)
        except Exception as e:
            logging.error('{}\nFolder or file not moved.'.format(e))
        try:
            _ = shutil.move(self.source_dir + '\\' + filename, self.destination_dir + '\\' + filename_base)
        except:
            pass

if __name__ == '__main__':
    process_bag_inst = ProcessBag(base_path=os.getcwd(),
                                  source_dir_name='bag_data',
                                  destination_dir_name=destination_directory_name,
                                  topic_list = ['/hub_0/sensor_0','/hub_0/sensor_1'])