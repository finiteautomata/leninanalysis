#/bin/sh
#asume que borraste las colecciones de lenin, por ejemplo, ejecutando un test
#mkdir dump
#mkdir dump/lenin
#wget ftp://lu000482:sakiraMI58@jmperez.com.ar/dump/lenin-with-iv/* -P dump/lenin
cd dump
mongorestore lenin
