# Lenin Analysis

## Setup

1. Clone the project
git clone git://github.com/geekazoid/leninanalysis
2. Install requirements

```
:~/leninanalysis$ [sudo] pip install -r requirements.txt

(Install pip installation: [sudo] apt-get install python-pip)
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


#Pipeline y estructuras de datos
2)reload_base_files() 
    espera lenin_work.json  
    crea id_lenin_work.json, crea by_year/YYYY_works.json para cada año 
    Agrega wid (work id) a cada trabajo 
    Hace un split de los trabajos por años y agrega yid (year id) a los trabajos  
        [ 
            { 
                wid,  
                name, 
                url,  
                text, 
                year, 
                month 
            } 
        ] 
        y 
        [ 
            { 
                wid,  
                yid,  
                name, 
                url,  
                text, 
                year, 
                month 
            } 
        ] 
3a)create_zipf_files()  
    espera by_year/YYYY_works.json  
    genera by_year/YYYY_zipf.json 
        [ 
            {yid, 
             wid, 
             name,  
             total_words,   #sin stopwords  
             total_vocab, 
             top_words, 
             top_words_with_ocurrences # [[w,c], [w,c]] 
            } 
        ]    
3b)create_zipf_resume() 
    espera lenin_work.json  
    genera years_zipf.json  
        [ 
            { 
                name,     #Es el año como string  
                total_words, #sin stopwords 
                total_vocab,  
                top_words,  
                top_words_with_ocurrences 
            } 
        ] 
    #Deberia cambiar a {$year: {name,total_words,total_vocab,top_words,top_words_with_ocurrences}}  
4)create_iv_files() 
    espera by_year/YYYY_works.json  
    configurar scales en iv.get_scales()  
    genera by_year/YYYY_iv.json 
     [  
        {    
         yid, 
         wid, 
         name,  
         best_iv_per_word,  
         best_scale,  
         best_window_size,  
         top_words, 
         top_words_with_iv, 
         total_words, #con stopwords  
         tried_windows  
         ivs, #[{iv_per_word,window_size,scale,top_words,top_words_with_iv}], 
        } 
 ]  
5)wna.wn_write()  
        espera by_year/YYYY_(works|iv|zipf).json  
        espera years_zipf.json  
        Genera by_year/YYYY_wn.json 
        {    
         praxis_iv, 
         theory_iv, 
         praxis_zipf, 
         theory_zipf, 
         zipf, #[{wid,yid,distances,theory, praxis}]  
         iv, #[{wid,yid,distances,theory, praxis}]  
         zipf_resume, #{distances,theory, praxis} 
          
        } 
