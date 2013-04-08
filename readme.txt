#Pipeline y estructuras de datos
1) crawl.bat 
	genera lenin_work.json
		[
			{
				name,
				url,
				text,
				year,
				month
			}
		]
	copiar a data_dir
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