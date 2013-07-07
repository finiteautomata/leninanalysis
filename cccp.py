#!/usr/bin/env python
# coding: utf-8
import config
import logging
import unittest
import argparse
import subprocess
from commands.database import populate_database
from commands.database import calculate_results
from commands.database import cleandb
from includes import preprocessor as pre
from includes import wn_analyzer as wna
from plot.window_sizes import plot_iv_things


reload(config)


JSON_SUBSET_NAME = "lenin_work.subset.json"
MIN_YEAR = config.MIN_YEAR
MAX_YEAR = config.MAX_YEAR

# Scraps ALL the works
def scrap_all_works():
    ret = subprocess.call("scrapy crawl lenin -o lenin_work.json -t json", shell=True)
    print "Scrapy has returned %s" % ret

# Scraps only a little subset for test purposes
def scrap_subset_of_works():
    try:
        min_year = MIN_YEAR
        max_year = MAX_YEAR
        ret = subprocess.call("scrapy crawl lenin_subset -o lenin_work_%s_%s.json -t json -a min_year=%d -a max_year=%d > log/subset.out" %(min_year, max_year, min_year, max_year), shell=True)
        print "Scrapy has returned %s" % ret
    except Exception as e:
        print "Something terrible happened during extraction of lenin subset: %s" % e


def run_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir="tests", pattern="*_tests.py")
    unittest.TextTestRunner(verbosity=2).run(test_suite)


def main():
    parser = argparse.ArgumentParser(description='Central de Control de Comandos y Procesos para el TP de Analisis de Lenin.')
    # Parameter to scrap all the works before or not
    parser.add_argument('--scrap', action='store_true', default=False, help='Scraps all the Lenin Works')
    parser.add_argument('--populate-database', action='store_true', default=False, help="From the scrapped works creates database called \"lenin\" (it assumes you're running MongoDB at localhost)")
    parser.add_argument('--scrap-subset', action='store_true', default=False, help='Scraps a little subset of the works of Lenin for test purposes')
    parser.add_argument('--split-years', action='store_true', default= False, help='Needs lenin_works.json, creates id_lenin_work.json and by_year/YYYY_works.json')
    parser.add_argument('--zipf', action='store_true', default= False, help='Needs by_year/YYYY_works.json, creates by_year/YYYY_zipf.json')
    parser.add_argument('--zipf-resume', action='store_true', default= False, help='Needs lenin_works.json, creates years_zipf.json')
    parser.add_argument('--iv', action='store_true', default= False, help='Needs by_year/YYYY_works.json, creates by_year/YYYY_iv.json')

    parser.add_argument('--wn', action='store_true', default= False, help='Needs by_year/YYYY_(works|iv|zipf).json and years_zipf.json, creates by_year/YYYY_wn.json')
    parser.add_argument('--restart-db', action='store_true', default= False, help='Executes split-years, zipf and zipf-resume')
    parser.add_argument('--plot-iv-analysis', action='store_true', default=False, help="Shows some plot about Information Value Analysis")
    parser.add_argument('--test', action='store_true', default=False, help="Run Tests")
    parser.add_argument('--calculate-results', action='store_true', default=False, help="Calculate Information Value Results for Documents")
    parser.add_argument('--cleandb', action='store_true', default=False, help="Cleans Database")

    # Parse args
    args = parser.parse_args()

    if args.scrap:
        scrap_all_works()
    if args.populate_database:
        populate_database()
    if args.scrap_subset:
        scrap_subset_of_works()
    if args.split_years:
        pre.reload_base_files(MIN_YEAR, MAX_YEAR+1)
    if args.zipf:
        pre.create_zipf_files(MIN_YEAR, MAX_YEAR+1)
    if args.zipf_resume:
        pre.create_zipf_resume(MIN_YEAR, MAX_YEAR+1)
    if args.iv:
        pre.create_iv_files(MIN_YEAR, MAX_YEAR+1)
    if args.wn:
        wna.create_wn_files(MIN_YEAR, MAX_YEAR+1)
    if args.restart_db:
        pre.restart_database(MIN_YEAR, MAX_YEAR+1)
    if args.plot_iv_analysis:
        plot_iv_things()
    if args.test:
        run_tests()
    if args.calculate_results:
        calculate_results()
    if args.cleandb:
        cleandb()

def init_logging():
    logger = logging.getLogger('lenin')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('lenin.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

if __name__ == "__main__":
    init_logging()
    main()
