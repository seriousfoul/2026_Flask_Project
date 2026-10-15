from models.Dbsystem import db
import time

"""

CREATE TABLE "downloads" (
	"downloadsid"	INTEGER,
	"name"	TEXT NOT NULL,
	"filepath"	TEXT NOT NULL,
	"size"	TEXT NOT NULL,
	"version"	TEXT NOT NULL,
	"info"	TEXT,
	"addtime"	INTEGER NOT NULL,
	"update"	INTEGER,
	PRIMARY KEY("downloadsid" AUTOINCREMENT)
);

"""

class Downloads(db.Model):    
    __tablename__ = "downloads"
    downloadsid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(30), nullable=False)
    version = db.Column(db.String(30), nullable=False)
    info = db.Column(db.Text)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default=lambda: int(time.time()))

    def __init__(self, name, filePath, size, version, info, addtime, lastUpdate):
        self.name = name
        self.filepath = filePath
        self.size = size
        self.version = version
        self.info = info
        self.addtime = addtime
        self.lastUpdate = lastUpdate