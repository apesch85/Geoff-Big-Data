#! /usr/bin/python

from sys import argv
import csv
from os import path
import re


error_message = ('Please provide full filepath to USGS Geomagnetism file as an '
                 'argument to be parsed.\n Example: "python data_averager.py '
              '/path/to/file"')
              
# The objective is to average all the Dst, the HON and the SJG columns only.
# The below variables are positional coordinates of this data we're interested
# in from the dataset provided.
#
# These values can be updated to calculate stats of other columns if desired.

dst_pos = 7
hon_pos = 10
sjg_pos = 11

def dataGrabber():
    """ This function ensures the file exists, and it is valid.
    
    A valid file is a USGS Gemoganetism .txt file downloaded from the USGS
    Geomagnetism website. It verifies it is a valid file by looking at the
    header row. If a valid file isn't provided, this script will not continue.
    
        Returns: geo_dataset - A list of lists with each inner list containing
            data from each row of the file.
    """
    
    geo_dataset = []
    
    # If an argument is not provided with the script, then print help text.
    
    if len(argv) != 2:
        print(error_message)
        
    # If an argument is provided, check that it is a valid, existing file.
    # If it is valid, clean up the extra white spaces.
    
    else:
        file_path = argv[1]
        if path.isfile(file_path):
            with open(file_path, 'r') as geo_data:
                geo_reader = csv.reader(geo_data, delimiter=' ')
                for row in geo_reader:
                    text_row = ' '.join(row)
                    clean_row = re.sub(' +', ' ',text_row)
                    geo_dataset.append([clean_row])
        else:
            print(error_message)
    if len(geo_dataset) < 1:
        print(error_message)
    else:
        if geo_dataset[0] == ['Year Mon Day Hr DOY from start Fractional DOY '
                              'Fractional year Dst HER KAK HON SJG sigma']:
            print('Valid dataset detected. Continuing...')
            return geo_dataset
        else:
            print(error_message)


def dataParser(usgs_geo_data):
    """ Takes a list of lists and finds the average of a subset of those lists.

    This function removes the header row which isn't data, and splits the sets
    of data we're interested in into each set into its own list. It then
    calculates the average (and other stats) of each set of data and prints 
    these averages to the terminal window.

    Arguments: 
        usgs_geo_data - A list of lists.
    """

    # All the lists used to sort nd calculate data.
    
    dst_list = []
    hon_list = []
    sjg_list = []
    bad_dst = []
    bad_hon = []
    bad_sjg = []
    
    just_data = usgs_geo_data[1:] # Remove header, leaving just data.
    
    for row in just_data:
        data_row = row[0].split(' ')
        dst_value = float(data_row[dst_pos])
        hon_value = float(data_row[hon_pos])
        sjg_value = float(data_row[sjg_pos])
        
        if dst_value != 99999.0:
            dst_list.append(dst_value)
        else:
            bad_dst.append(dst_value)
        if hon_value != 99999.0:
            hon_list.append(hon_value)
        else:
            bad_hon.append(hon_value)
        if sjg_value != 99999.0:
            sjg_list.append(sjg_value)
        else:
            bad_sjg.append(sjg_value)
        
    dst_average = sum(dst_list) / len(dst_list)
    hon_average = sum(hon_list) / len(hon_list)
    sjg_average = sum(sjg_list) / len(sjg_list)
 
    print('\nDST average: %s' % dst_average)
    print('HON average: %s' % hon_average)
    print('SJG average: %s' % sjg_average) 

    print('\nDST max: %s' % max(dst_list))
    print('HON max: %s' % max(hon_list))
    print('SJG max: %s' % max(sjg_list)) 
    
    print('\nDST min: %s' % min(dst_list))
    print('HON min: %s' % min(hon_list))
    print('SJG min: %s' % min(sjg_list)) 
    
    print('\nBad DST value count: %s' % len(bad_dst))
    print('Bad HON value count: %s' % len(bad_hon))
    print('Bad SJG value count: %s' % len(bad_sjg))
    
    print('\nTotal DST value count: %s' % len(dst_list))
    print('Total HON value count: %s' % len(hon_list))
    print('Total SJG value count: %s' % len(sjg_list))


def main():
    """ Execute other functions.
    
    If dataGrabber returns something, execute dataParser. Otherwise, stop.
    """
    
    usgs_data_list = dataGrabber()
    if usgs_data_list:
        dataParser(usgs_data_list)
    
    
if __name__ == '__main__':
    main()