from models.Dbsystem import db
import time

"""
CREATE TABLE "homepage_banner" (
	"bannerid"	INTEGER,
	"name"	TEXT,
	"imgpath"	TEXT NOT NULL,
	"enable"	INTEGER NOT NULL DEFAULT 1,
	"addtime"	INTEGER NOT NULL,
	PRIMARY KEY("bannerid" AUTOINCREMENT)
);
"""

class Banner(db.Model):
    __tablename__ = "homepage_banner"
    bannerid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    imgpath = db.Column(db.String(100), nullable=False)
    enable = db.Column(db.Boolean, default=True, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    
    def __init__(self, name, imgPath, enable, addtime):
        self.name = name
        self.imgpath = imgPath
        self.enable = enable
        self.addtime = addtime