#! /usr/bin/python

from sys import argv
import csv
from os import path
import re


error_message = ('Please provide full filepath to USGS Geomagnetism file as an '
                 'argument to be parsed.\n Example: "python data_averager.py '
              '/path/to/file"')

# The objective is to categorize the Dst values for the earthly average, HON and SJG.
# The below variables are positional coordinates of this data we're interested
# in from the dataset provided.

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

    dstSuperstormCount = 0
    dstIntenseStormCount = 0
    dstModerateStormCount = 0
    dstWeakStormCount = 0
    dstBelowAverageCount = 0
    dstAverageCount = 0
    dstAboveAverageCount = 0
    dstFarAboveAverageCount = 0
    dstAbove38Count = 0
    honSuperstormCount = 0
    honIntenseStormCount = 0
    honModerateStormCount = 0
    honWeakStormCount = 0
    honBelowAverageCount = 0
    honAverageCount = 0
    honAboveAverageCount = 0
    honFarAboveAverageCount = 0
    honAbove38Count = 0
    sjgSuperstormCount = 0
    sjgIntenseStormCount = 0
    sjgModerateStormCount = 0
    sjgWeakStormCount = 0
    sjgBelowAverageCount = 0
    sjgAverageCount = 0
    sjgAboveAverageCount = 0
    sjgFarAboveAverageCount = 0
    sjgAbove38Count = 0

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
        
        # Categorizer      
  
        if dst_value < -250:
            dstSuperstormCount += 1
        else if dst_value > -251 | < -100:
            dstIntenseStormCount += 1
        else if dst_value > -101 | < -49:
            dstModerateStormCount += 1
        else if dst_value > -50 | < -29:
            dstWeakStormCount += 1
        else if dst_value > -30 | < -9:
            dstBelowAverageCount += 1 
        else if dst_value > -10 | < 11:
            dstAverageCount += 1
        else if dst_value > 10 | < 31:
            dstAboveAverageCount += 1
        else if dst_value > 30 | < 39:
            dstFarAboveAverageCount += 1
        else dst_list.append(dst_value) > 38:
            dstAbove38Count += 1

        if hon_value < -250:
            honSuperstormCount += 1
        else if hon_value > -251 | < -100:
            honIntenseStormCount += 1
        else if hon_value > -101 | < -49:
            honModerateStormCount += 1
        else if hon_value > -50 | < -29:
            honWeakStormCount += 1
        else if hon_value > -30 | < -9:
            honBelowAverageCount += 1 
        else if hon_value > -10 | < 11:
            honAverageCount += 1
        else if hon_value > 10 | < 31:
            honAboveAverageCount += 1
        else if hon_value > 30 | < 39:
            honFarAboveAverageCount += 1
        else hon_list.append(hon_value) > 38:
            honAbove38Count += 1

        if sjg_value < -250:
            sjgSuperstormCount += 1
        else if sjg_value > -251 | < -100:
            sjgIntenseStormCount += 1
        else if sjg_value > -101 | < -49:
            sjgModerateStormCount += 1
        else if sjg_value > -50 | < -29:
            sjgWeakStormCount += 1
        else if sjg_value > -30 | < -9:
            sjgBelowAverageCount += 1 
        else if sjg_value > -10 | < 11:
            sjgAverageCount += 1
        else if sjg_value > 10 | < 31:
            sjgAboveAverageCount += 1
        else if sjg_value > 30 | < 39:
            sjgFarAboveAverageCount += 1
        else sjg_list.append(sjg_value) > 38:
            sjgAbove38Count += 1
            
    print('\n Average Dst Super-storms: %s' % dstSuperstormCount)
    print('Average Dst Intense Storm Count: %s' % dstIntenseStormCount)
    print('Average Dst Moderate Storm Count: %s' % dstModerateStormCount)
    print('Average Dst Weak Storm Count: %s' % dstWeakStormCount)
    print('Average Dst Below Average Count: %s' % dstBelowAverageCount)
    print('Average Dst Average Count: %s' % dstAverageCount)
    print('Average Dst Above Average Count: %s' % dstAboveAverageCount)
    print('Average Dst Above 38 Count: %s' % dstAbove38Count)

    print('\n Average HON Super-storms: %s' % honSuperstormCount)
    print('Average HON Intense Storm Count: %s' % honIntenseStormCount)
    print('Average HON Moderate Storm Count: %s' % honModerateStormCount)
    print('Average HON Weak Storm Count: %s' % honWeakStormCount)
    print('Average HON Below Average Count: %s' % honBelowAverageCount)
    print('Average HON Average Count: %s' % honAverageCount)
    print('Average HON Above Average Count: %s' % honAboveAverageCount)
    print('Average HON Above 38 Count: %s' % honAbove38Count)

    print('\n Average SJG Super-storms: %s' % sjgSuperstormCount)
    print('Average SJG Intense Storm Count: %s' % sjgIntenseStormCount)
    print('Average SJG Moderate Storm Count: %s' % sjgModerateStormCount)
    print('Average SJG Weak Storm Count: %s' % sjgWeakStormCount)
    print('Average SJG Below Average Count: %s' % sjgBelowAverageCount)
    print('Average SJG Average Count: %s' % sjgAverageCount)
    print('Average SJG Above Average Count: %s' % sjgAboveAverageCount)
    print('Average SJG Above 38 Count: %s' % sjgAbove38Count)

    
    # Other Table Values

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
