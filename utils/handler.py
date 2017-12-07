"""
Module that offers some common utility methods
"""
import shutil
import csv
import os


def convert_json_to_csv(json_data, temp_folder, temp_file_name):
    """
    Convert the json data into a csv and save in a tmp file
    then return the filename
    """
    print('Converting file to csv...')
    # open a file for writing
    temp_file = open('{}{}.csv'.format(temp_folder, temp_file_name), 'w')
    # create the csv writer object
    csv_writer = csv.writer(temp_file)
    count = 0
    for data in json_data:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    temp_file.close()
    return '{}{}.csv'.format(temp_folder, temp_file_name)

def empty_tmp_folder(dir_name):
    """
    Delete all the contents of the given directory
    """
    for _f in os.listdir(dir_name):
        os.remove(dir_name+_f)
