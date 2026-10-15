from models.Dbsystem import db
import time

"""

CREATE TABLE "faq" (
	"fagid"	INTEGER,
	"question"	TEXT NOT NULL,
	"answer"	TEXT NOT NULL,
	"addtime"	INTEGER NOT NULL,
	"update"	INTEGER,
	PRIMARY KEY("fagid" AUTOINCREMENT)
);

"""

class Faq(db.Model):    
    __tablename__ = "faq"
    faqid = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default= lambda: int(time.time()))
   
    def __init__(self, question, answer, addtime, lastUpdate):
        self.question = question
        self.answer = answer
        self.addtime = addtime
        self.lastUpdate = lastUpdate