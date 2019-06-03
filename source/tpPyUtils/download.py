#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utilities functions for downloading files
"""

from __future__ import print_function, division, absolute_import

import os
import re
import shutil
import urllib2
import zipfile

numbers = re.compile('\d+')


def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    print("Downloaded %d of %d bytes (%0.2f%%)\r" % (bytes_so_far, total_size, percent))
    if bytes_so_far >= total_size:
        print('\n')


def chunk_read(response, destination, chunk_size=8192, report_hook=None):
    with open(destination, 'ab') as dst_file:
        total_size = response.info().getheader('Content-Length').strip()
        total_size = int(total_size)
        bytes_so_far = 0
        while 1:
            chunk = response.read(chunk_size)
            dst_file.write(chunk)
            bytes_so_far += len(chunk)
            if not chunk:
                break
            if report_hook:
                report_hook(bytes_so_far=bytes_so_far, chunk_size=chunk_size, total_size=total_size)
    dst_file.close()
    return bytes_so_far


def download_file(filename, destination):
    print('Downloading file {0} to temporary folder -> {1}'.format(os.path.basename(filename), destination))
    try:
        dst_folder = os.path.dirname(destination)
        if not os.path.exists(dst_folder):
            print('Creating downloaded folders ...')
            os.makedirs(dst_folder)

        hdr = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'}
        req = urllib2.Request(filename, headers=hdr)
        data = urllib2.urlopen(req)
        chunk_read(response=data, destination=destination, report_hook=chunk_report)
    except Exception as e:
        raise e

    if os.path.exists(destination):
        print('Files downloaded succesfully!')
        return True
    else:
        print('ERROR: Error when downloading files. Maybe server is down! Please contact TD!')
        return False


def unzip_file(filename, destination, removeFirst=True, removeSubfolders=None):
    print('Unzipping file {} to --> {}'.format(filename, destination))
    try:
        if removeFirst and removeSubfolders:
            print('Removing old installation ...')
            for subfolder in removeSubfolders:
                p = os.path.join(destination, subfolder)
                print('\t{}'.format(p))
                if os.path.exists(p):
                    shutil.rmtree(p)
        if not os.path.exists(destination):
            print('Creating destination folders ...')
            os.makedirs(destination)
        zip_ref = zipfile.ZipFile(filename, 'r')
        zip_ref.extractall(destination)
        zip_ref.close()
        print('Unzip completed!')
    except Exception as e:
        raise e


def get_version(s):
    """
    Look for the last sequence of number(s) in a string and increment
    """

    if numbers.findall(s):
        lastoccr_sre = list(numbers.finditer(s))[-1]
        lastoccr = lastoccr_sre.group()
        return lastoccr
    return None