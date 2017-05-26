from rfp_service import *
from receipt import *
from secret import *
from datetime import date

from tinydb import TinyDB, Query

if __name__ == '__main__':
	# Handle DUO Count
	db = TinyDB('keys.json')
	Duos = Query()
	res = db.search(Duos.secret == DUO_SECRET)
	c = 0
	if len(res) == 0:
		db.insert({'secret': DUO_SECRET, 'count': 0})
	else:
		c = res[0]['count']
		db.update({'count': c+1}, Duos.secret == DUO_SECRET)

	receipts = [
		Receipt(date=date(2017, 3, 26), amount=9.50, notes='Amazon', filename="D:/Documents/MIT/ProjX/Receipts/amazon.pdf"),
		Receipt(date=date(2017, 3, 26), amount=9.50, notes='Amazon', filename="D:/Documents/MIT/ProjX/Receipts/amazon.pdf")
	]

	submit_rfp(USERNAME, PASSWORD, DUO_SECRET, c, 'Test RFP', '2859935', '420319', 'Shreyas Kapur', receipts)
