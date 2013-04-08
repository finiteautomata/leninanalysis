scrapy crawl lenin -o lenin_work.json -t json
scrapy parse --spider=lenin -v --depth=2 --callback=parse_indexed_work http://www.marxists.org/archive/lenin/works/1917/staterev/index.htm

