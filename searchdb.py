import pickle
import sys
import pprint

dbfile = "resistent.saved"

def searchdb(keysearch="nom",valuesearch="verillon"):
	results = []
	keysearch=sys.argv[1]
	
	if sys.argv.__len__() == 2:
		for keys in db:
			results.append(db[keys].get(keysearch))
	else: 
		valuesearch=sys.argv[2]
		for keys in db:
			if str(db[keys].get(keysearch)).casefold().count(valuesearch.casefold()) > 0:
				results.append(db[keys])
			
	return results

if __name__ == '__main__':
	
	input = open(dbfile,"rb")
	db = pickle.load(input)
	
	resultats = searchdb()
	
	pprint.pprint(resultats,indent=3)
	print(resultats.__len__(), "/", db.__len__())
		
	
	
	
	
	

