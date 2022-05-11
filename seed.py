from csv import DictReader
from app import db
from models import Printer, Filament, User, Post

db.drop_all()
db.create_all()

user = User(username='3dpfl',password='$2b$12$Wra61dnEC3oTIHOoLU3NPOVZXOg7fmmkP1R6HBPddep8MJ9V062xu')
db.session.add(user)
db.session.commit()

with open('seed/printers.csv') as printers:
    db.session.bulk_insert_mappings(Printer, DictReader(printers))

with open('seed/filaments.csv') as filaments:
    db.session.bulk_insert_mappings(Filament, DictReader(filaments))

posts2 = []
with open('seed/posts.csv') as posts1:
    for row in DictReader(posts1):
        posts2.append(row)

posts3 = []
for row in posts2:
    newrow = {}
    for key in row:
        if row[key] == "False":
            newrow[key] = False
        elif row[key] == "True":
            newrow[key] = True
        else:
            newrow[key] = row[key]
    posts3.append(newrow)

db.session.bulk_insert_mappings(Post, posts3)
db.session.commit()
