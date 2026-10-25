from models.Dbsystem import db
import time
"""

CREATE TABLE "contactus_message" (
	"messageid"	INTEGER,
	"formid"	INTEGER NOT NULL,
	"read"	INTEGER NOT NULL DEFAULT 0,
	"processed"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("messageid" AUTOINCREMENT),
	FOREIGN KEY("formid") REFERENCES "contactus_form"("formid")
);


"""

class Message(db.Model):    
    __tablename__ = "contactus_message"
    messageid = db.Column(db.Integer, primary_key=True)
    formid = db.Column(db.Integer, nullable=False)
    read = db.Column(db.Boolean, default=False, nullable=False)
    processed = db.Column(db.Boolean, default=False, nullable=False)
    lastUpdate = db.Column(db.Integer, default=lambda: int(time.time()))

    def __init__(self, formid, read, processed, lastUpdate):
        self.formid = formid
        self.read = read
        self.processed = processed
        self.lastUpdate = lastUpdate
