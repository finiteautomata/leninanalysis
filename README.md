# Lenin Analysis

## Setup

1. Clone the project
git clone git://github.com/geekazoid/leninanalysis
2. Install requirements

```
:~/leninanalysis$ [sudo] pip install -r requirements.txt

(Install pip: [sudo] apt-get install python-pip)
```
3. Edit config.py. Change `data_dir` to point to the absolute path of your data directory. This is where all the scrapped JSONs will be saved in.

Also, you can set MIN_YEAR and MAX_YEAR to scrap smaller subsets of Lenin Full Works. 

For instance:

```
data_dir="/home/marat/Dropbox/Facu/incc/incc-2012/TP Lenin/data/"
MIN_YEAR = 1900
MAX_YEAR = 1905
WNA_VERBOSE = 1
``` 
4. Scrap lenin works.

```
$ python cccp.py --scrap
``` 
This command creates a file named lenin_work.json at the root directory of the project.

You can also scrap a smaller subset with:
```
$ python cccp.py --scrap
``` 

5. Populate mongodb with scrapped data (creates collection lenin.document)
```
$ ./cccp.py --populate-database
``` 

5. Run Information Value analysis over the documents (creates collection lenin.information_value_result)
```
$ ./cccp.py --calculate-results
``` 