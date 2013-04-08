#!/usr/bin/python
# coding: utf-8
import argparse
import subprocess
from includes import preprocessor

JSON_SUBSET_NAME = "lenin_work.subset.json"

# Scraps ALL the works
def scrap_all_works():
    ret = subprocess.call("scrapy crawl lenin -o lenin_work.json -t json", shell=True)
    print "Scrapy has returned %s" % ret

# Scraps only a little subset for test purposes
def scrap_subset_of_works():
    try:

        ret = subprocess.call("scrapy crawl lenin_subset -o %s -t json > log/subset.out" %(JSON_SUBSET_NAME), shell=True)
        print "Scrapy has returned %s" % ret 
        if not ret:
            subprocess.call("ls -alh")
            subprocess.call("mv %s data/" % JSON_SUBSET_NAME)
    except Exception as e:
        print "Something terrible happened during extraction of lenin subset: %s" % e

def main():
    parser = argparse.ArgumentParser(description='Comité Central para el TP de Analisis de Lenin.')
    # Parameter to scrap all the works before or not
    parser.add_argument('--scrap', action='store_true', default=False, help='Scraps all the Lenin Works')
    parser.add_argument('--scrap-subset', action='store_true', default=False, help='Scraps a little subset of the works of Lenin for test purposes')
    # Parse args
    args = parser.parse_args()

    if args.scrap:
        scrap_all_works()
    if args.scrap_subset:
        scrap_subset_of_works()

    print args.scrap
    print args.scrap_subset


if __name__ == "__main__":
    main()

