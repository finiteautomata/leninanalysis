#!/usr/bin/env python
# coding: utf-8
import config
import logging
import argparse
import subprocess
from commands.database import populate_database
from commands.database import calculate_results
from commands.database import cleandb
from includes import preprocessor as pre
from analyzers import wn_analyzer as wna
from plot.window_sizes import plot_iv_things


reload(config)


JSON_SUBSET_NAME = "lenin_work.subset.json"

# Scraps ALL the works
def scrap_all_works():
    ret = subprocess.call("scrapy crawl lenin -o lenin_work.json -t json", shell=True)
    print "Scrapy has returned %s" % ret



def main():
    parser = argparse.ArgumentParser(description='Central de Control de Comandos y Procesos para el TP de Analisis de Lenin.')
    # Parameter to scrap all the works before or not
    parser.add_argument('--scrap', action='store_true', default=False, help='Scraps all the Lenin Works')
    parser.add_argument('--populate-database', action='store_true', default=False, help="From the scrapped works creates database called \"lenin\" (it assumes you're running MongoDB at localhost)")
    parser.add_argument('--plot-iv-analysis', action='store_true', default=False, help="Shows some plot about Information Value Analysis")
    parser.add_argument('--calculate-results', action='store_true', default=False, help="Calculate Information Value Results for Documents")

    # Parse args
    args = parser.parse_args()

    if args.scrap:
        scrap_all_works()
    if args.populate_database:
        populate_database()
    if args.plot_iv_analysis:
        plot_iv_things()
    if args.calculate_results:
        calculate_results()

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
