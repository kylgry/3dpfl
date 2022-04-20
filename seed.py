from csv import DictReader
from app import db
from models import PrinterBrand, Printer

db.drop_all()
db.create_all()

with open('data/printerbrands.csv') as printerbrands:
    db.session.bulk_insert_mappings(PrinterBrand, DictReader(printerbrands))

db.session.commit()

with open('data/printers.csv') as printers:
    db.session.bulk_insert_mappings(Printer, DictReader(printers))

db.session.commit()
