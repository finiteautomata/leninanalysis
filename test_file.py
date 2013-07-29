#Fake python file
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
from pymongo import MongoClient
from information_value import models
from bson.objectid import ObjectId


def war_and_rev():
	client = MongoClient()
	db = client.lenin
	model_it = models.Document.query.find({'name': {'$regex': '.*State.*'}}, {'text':0})
	state_it = db.document.find({'name': {'$regex': '.*State.*'}}, {'text':0})

	return state_it
	#war_and_rev = models.Document.query.find({'_id': ObjectId("51e87f673092073a3fc5a026")}).first()
	#print str(model_it.count())
	#print str(state_it.count())
	return war_and_rev