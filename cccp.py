#!/usr/bin/env python
# coding: utf-8
import sys
import config
import logging
import argparse
import subprocess

import ming

reload(config)


# Scraps ALL the works
def scrap_all_works():
    ret = subprocess.call("scrapy crawl lenin -o lenin_work.json -t json", shell=True)
    print "Scrapy has returned %s" % ret



def main():
    parser = argparse.ArgumentParser(description='Central de Control de Comandos y Procesos para el TP de Analisis de Lenin.')
    # Parameter to scrap all the works before or not
    parser.add_argument('--shell', action='store_true', default=False, help="Opens an ipython console with db configured")
    parser.add_argument('--scrap', action='store_true', default=False, help='Scraps all the Lenin Works')
    parser.add_argument('--populate-database', action='store_true', default=False, help="From the scrapped works creates database called \"lenin\" (it assumes you're running MongoDB at localhost)")
    parser.add_argument('--plot', action='store_true', default=False, help="Add this flag for plotting")
    parser.add_argument('--analysis', action='store_true', default=False, help="Add this flag for results calculation")
    parser.add_argument('--plot-iv-analysis', action='store_true', default=False, help="Shows some plot about Information Value Analysis")
    parser.add_argument('--window_size_generator', default='WindowsHardCodedSizeGenerator', help="Select a Window Size generator Algorhitm")
    parser.add_argument('--calculate-results', action='store_true', default=False, help="Calculate Information Value Results for Documents")
    parser.add_argument('--documents', nargs='+', metavar=('name'), help='Selects documents from name regex')
    parser.add_argument('--notebook-server', action='store_true', default=False, help='Starts notebook server')
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    # Parse args
    args = parser.parse_args()

    if args.scrap:
        scrap_all_works()
    if args.populate_database:
        from commands.database import populate_database
        populate_database()
    if args.plot_iv_analysis:
        from plot.window_sizes import plot_iv_things
        plot_iv_things()
    if args.calculate_results:
        from commands.database import calculate_results
        calculate_results()

    doc_list = None
    if args.documents:
        from information_value.models import DocumentList
        doc_list = DocumentList(args.documents[0])
    if args.analysis:
        from commands.database import calculate_results
        documents = None
        if doc_list:
            documents = doc_list.documents
        calculate_results(documents=documents, window_size_algorithm=args.window_size_generator)
    if args.plot:
        from plot import window_sizes
        window_sizes.plot_scale_vs_information(doc_list.documents)
        #window_sizes.plot_len_vs_most_informative(doc_list.documents)
    if args.notebook_server:
        subprocess.call("ipython notebook --notebook-dir=notebooks", shell=True)
    if args.shell:
        subprocess.call("ipython -i interpreter.py", shell=True)


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
    ming_config = {'ming.document_store.uri': config.DATABASE_URL}
    ming.configure(**ming_config)

    init_logging()
    main()
