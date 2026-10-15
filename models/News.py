from models.Dbsystem import db
import time

"""

CREATE TABLE "news" (
	"newsid"	INTEGER,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER NOT NULL,
	"lastUpdated"	INTEGER,
	PRIMARY KEY("newsid" AUTOINCREMENT)
);


"""


class News(db.Model):    
    __tablename__ = "news"
    newsid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default= lambda: int(time.time()))

    def __init__(self, title, content, addtime, lastUpdate):
        self.title = title
        self.content = content
        self.addtime = addtime
        self.lastUpdate = lastUpdate