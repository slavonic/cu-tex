#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function

import argparse
import zipfile
import fnmatch
import collections
import os

class ZipUri(collections.namedtuple('ZipUri', ['text', 'file', 'path'])):
    
    def __new__(cls, text):
        
        if ':' in text:
            file, path = text.split(':')
        else:
            file, path = None, text

        return super(ZipUri, cls).__new__(cls, text, file, path)


def main(args):
    source_uri = ZipUri(args.source)
    target_uri = ZipUri(args.target)

    if source_uri.file is None:
        with open(source_uri.path, 'r') as szip:
            sbytes = szip.read()
        name = os.path.basename(source_uri.path)
        with zipfile.ZipFile(target_uri.file, 'a', compression=zipfile.ZIP_DEFLATED) as tzip:
            if target_uri.path == '' or target_uri.path[-1] == '/':
                tname = target_uri.path + os.path.basename(name)
            else:
                tname = target_uri.path
            tzip.writestr(tname, sbytes)
            print('copying:', name, tname)
    else:
        with zipfile.ZipFile(source_uri.file, 'r') as szip:
            with zipfile.ZipFile(target_uri.file, 'a', compression=zipfile.ZIP_DEFLATED) as tzip:
                for name in szip.namelist():
                    if source_uri.path == '' or fnmatch.fnmatch(name, source_uri.path):
                        sbytes = szip.read(name)
                        
                        if target_uri.path == '' or target_uri.path[-1] == '/':
                            tname = target_uri.path + os.path.basename(name)
                        else:
                            tname = target_uri.path
                        tzip.writestr(tname, sbytes)
                        print('copying:', name, tname)

    return 0


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Copy files from zip to zip (supports masks and recursion)')
    parser.add_argument('source', help='Source file specification. Use slashes to indicate path inside zip')
    parser.add_argument('target', help='Source file specification. Use slashes to indicate path inside zip')
    
    args = parser.parse_args()
    
    parser.exit(main(args))
