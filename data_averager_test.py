#! /usr/bin/python

import pytest
import data_averager
from mock import patch

def test_dataGrabberFail():

    fail_tests = [10, {'test': 1}, ['test'], '/some/path/to/somewhere']
    
    with patch.object(sys, 'argv', fail_tests):
        averager_result = data_averager.dataGrabber()
        assert averager_result == None


def test_dataGrabberPass():
    
    working_sample = [
        ['Year Mon Day Hr DOY from start Fractional DOY '
         'Fractional year Dst HER KAK HON SJG sigma'],
        ['1958 1 1 1 0.10208333333E+01 0.10208333333E+01 0.19580000571E+04 '
         '-113.6 -126.4 -86.1 -89.0 -152.8 31.9'], 
        ['1958 1 1 2 0.10625000000E+01 0.10625000000E+01 0.19580001712E+04 '
         '-104.3 -117.3 -78.4 -90.4 -130.9 24.1']
    ]
    
    averager_result = data_averager.dataGrabber()
    assert type(averager_result) == list
    assert len(averager_result) >= 1
    assert averager_result[0] == [
        'Year Mon Day Hr DOY from start Fractional DOY Fractional year Dst HER '
        'KAK HON SJG sigma'
        ]