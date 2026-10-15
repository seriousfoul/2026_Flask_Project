from models.Dbsystem import db
import time

"""
CREATE TABLE "homepage_info" (
	"infoid"	INTEGER,
	"title"	TEXT NOT NULL,
	"imgpath"	TEXT NOT NULL,
	"enable"	INTEGER NOT NULL DEFAULT 1,
	"addtime"	INTEGER NOT NULL,
	PRIMARY KEY("infoid" AUTOINCREMENT)
);
"""

class Info(db.Model):
    __tablename__ = "homepage_info"
    infoid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    imgpath = db.Column(db.String(100), nullable=False)
    enable = db.Column(db.Boolean, default=True)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    
    def __init__(self, title, imgPath, enable, addtime):
        self.title = title
        self.imgpath = imgPath
        self.enable = enable
        self.addtime = addtime