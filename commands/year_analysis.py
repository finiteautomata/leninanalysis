#! coding: utf-8
from analyzers.year_analyzer import YearAnalyzer 

def calculate_year_analysis(min_year, max_year, concepts):
    analyzer = YearAnalyzer(concepts)

    for year in xrange(min_year, max_year+1):
        res = analyzer.analyze_year(year)
        print res
