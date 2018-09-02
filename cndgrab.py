from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import os.path
import collections
import signal
import sys

resurls =  []
dbfilename = "resistent.saved"
# ~ db = {}

champs = [("nom",'{"class":u"flexi value field_nom"}'),
("prenom",'{"class":u"flexi value field_prenom"}'),
("csp",'{"class":u"flexi value field_csp"}'),
("sexe",'{"class":u"flexi value field_sexe"}'),
("ddn",'{"class":u"flexi value field_ddn"}'),
("situation",'{"class":u"flexi value fiel_situation"}'),
("dateenregistrement",'{"class":u"flexi value field_dateenregistrement"}'),
("fonction",'{"class":u"flexi value field_fonction"}'),
("reseau",'{"class":u"flexi value field_reseau"}'),
("suite",'{"class":u"flexi value field_suite"}'),
("ta",'{"class":u"flexi value field_ta"}'),
("pseudo",'{"class":u"flexi value field_pseudo"}'),
("numeroagent",'{"class":u"flexi value field_numagent"}'),
("datefinaction",'{"class":u"flexi value field_datefinaction"}'),
("raison",'{"class":u"flexi value field_raison"}')]

i = 0

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        dump_db()
        sys.exit(0)

def dbexisting():
	if os.path.isfile(dbfilename) is True and os.path.getsize(dbfilename) > 0:
		return True

def load_db():
		dbfile = open(dbfilename,"rb")
		db = pickle.load(dbfile)
		dbfile.close
		print('Db Loaded')
		return db

		
def dump_db():
	print("Writing DB")
	dbfile = open(dbfilename,"wb")
	pickle.dump(db,dbfile)
	dbfile.flush()
	dbfile.close()

def check_url():
	if str(link.get('href')) in db:
		return True	
 
if __name__ == '__main__':
	
	signal.signal(signal.SIGINT, signal_handler)
	
	if dbexisting():
		db = load_db()
	else:
		db={}
		
	urlroot = 'http://cnd-castille.org/index.php/3-base-de-donnees/resistant/'
	pageroot = urlopen(urlroot)
	souproot = BeautifulSoup(pageroot,'html.parser')
	resurls=souproot.find('table').find_all('a')
	
	for link in resurls:
		
		if check_url():
			print("Doublon")
			i += 1
			continue
			
		temp = 'http://cnd-castille.org'+ str(link.get('href'))
		print("\n Processing link : ", i, '/', len(resurls))
		print("URL = ", temp, '\n')
		page = urlopen(temp)
		soup = BeautifulSoup(page,'html.parser')
		thisres={}
			
		print('Adding:', end= " ")
		for x,y in champs:			
		
			if soup.find('div',attrs=(eval(y))) is not None:
				thisres[x] = soup.find('div',attrs=(eval(y))).getText()
				print(x,' = ', thisres[x], ',', end=" ")		
			else:
				thisres[x] = None
				print(x,' = ', thisres[x], ',', end=" ")		
		
		db[str(link.get('href'))] = thisres
		print('\n Done \n')
		i += 1

	dump_db()

