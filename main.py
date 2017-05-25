from rfp_service import *
from secret import *

from tinydb import TinyDB, Query

if __name__ == '__main__':
	db = TinyDB('keys.json')
	Duos = Query()
	res = db.search(Duos.secret == DUO_SECRET)
	c = 0
	if len(res) == 0:
		db.insert({'secret': DUO_SECRET, 'count': 0})
	else:
		c = res[0]['count']
		db.update({'count': c+1}, Duos.secret == DUO_SECRET)

	submit_rfp(USERNAME, PASSWORD, DUO_SECRET, c, 'Test', None)
