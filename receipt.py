import datefinder
import datetime
import invoice2data.in_pdftotext as pdftotext

class Receipt(object):

	def __init__(self, date, amount, tax=0):
		self.date = date
		self.amount = amount
		self.tax = tax

	def get_rfp_amount(self):
		return self.amount - self.tax

# Takes a PDF invoice and returns a guess.
# Does this in a kinda horrible way.
def parse_pdf(filename):
	invoice_text = pdftotext.to_text(filename).decode('utf-8')
	matches = datefinder.find_dates(invoice_text)
	# This is where my amazing heuristics start.
	# Pick first match that is within current 2 years?
	today = datetime.datetime.now()
	for m in matches:
		days = (today - m).days
		print days