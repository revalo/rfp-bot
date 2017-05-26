import datefinder
import datetime
import invoice2data.in_pdftotext as pdftotext

class Receipt(object):

	def __init__(self, date, amount, filename, notes, tax=0):
		self.date = date
		self.amount = amount
		self.tax = tax
		self.filename = filename
		self.notes = notes

	def get_amount(self):
		return self.amount - self.tax

# Takes a PDF invoice and returns a guess.
# Does this in a kinda horrible way.
# Not finished.
def parse_pdf(filename):
	raise NotImplementedError

	invoice_text = pdftotext.to_text(filename).decode('utf-8')
	matches = datefinder.find_dates(invoice_text)
	# This is where my amazing heuristics start.
	# Pick first match that is within current 2 years?
	today = datetime.datetime.now()
	for m in matches:
		days = (today - m).days

