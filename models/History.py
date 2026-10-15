from models.Dbsystem import db
import time

"""

CREATE TABLE "homepage_history" (
	"historyid"	INTEGER,
	"title"	TEXT,
	"content"	TEXT,
	"addtime"	INTEGER,
	"update"	INTEGER,
	PRIMARY KEY("historyid" AUTOINCREMENT)
);

"""

class History(db.Model):
    __tablename__ = "homepage_history"
    historyid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default= lambda: int(time.time()))

    def __init__(self, title, content, addtime, lastUpdate):
        self.title = title
        self.content = content
        self.addtime = addtime
        self.lastUpdate = lastUpdate