import os
import re
import datetime

stamp_re = re.compile(
    r'^([^-]*)(-bench)?-(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})(.xml)?$')

def list_stamps(directory):
    for path in os.listdir(directory):
        match = stamp_re.match(path)
        if match is not None:
            yield path

def get_datetime(path):
    return datetime.datetime(
        *map(int, stamp_re.match(path).groups()[2:-1]))

def sorted_stamps(directory):
    return sorted(
        ((get_datetime(stamp), stamp)
         for stamp in list_stamps(directory)),
        reverse=True)
