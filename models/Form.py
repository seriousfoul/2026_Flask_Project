from models.Dbsystem import db
import time

"""

CREATE TABLE "contactus_form" (
	"formid"	INTEGER,
	"companyname"	TEXT,
	"contactname"	TEXT NOT NULL,
	"address"	TEXT,
	"phone"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER NOT NULL,
	PRIMARY KEY("formid" AUTOINCREMENT)
);

"""

class Form(db.Model):    
    __tablename__ = "contactus_form"
    formid = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(30))
    contactname = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    
    def __init__(self, companyname, contactname, email, address, phone, title, content, addtime):
        self.companyname = companyname
        self.contactname = contactname
        self.email = email
        self.address = address
        self.phone = phone
        self.title = title
        self.content = content
        self.addtime = addtime        