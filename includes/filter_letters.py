from information_value.models import odm_session
from information_value.models import Document
from information_value.models import InformationValueResult


def letter_criterion(doc):
	length = len(doc.text)
	if "TO" in doc.name:
		if "HIS MOTHER" in doc.name: #aca caen 44/3261
			return False 
		elif "HIS SISTER" in doc.name: #aca caen 10
			return False
		else: #775/3261
			#print str(len(doc.text))+ " "+doc.name
			return True
	else:
		return True

def filter_letters():
	all_docs = Document.query.find(dict())
	filtered_docs = filter(letter_criterion, all_docs)
	return filtered_docs