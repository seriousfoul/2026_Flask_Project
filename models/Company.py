from models.Dbsystem import db

"""

CREATE TABLE "contactus_company" (
	"name"	TEXT,
	"address"	TEXT NOT NULL,
	"phone"	TEXT NOT NULL,
	"fax"	TEXT,
	"email"	TEXT,
	"servicetime"	TEXT,
	PRIMARY KEY("name")
);

"""

class Company(db.Model):    
    __tablename__ = "contactus_company"
    name = db.Column(db.String(30), primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    fax = db.Column(db.String(20))    
    servicetime = db.Column(db.Text)
    
    def __init__(self, name, email, address, phone, fax, servicetime):
        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        self.fax = fax
        self.servicetime = servicetime