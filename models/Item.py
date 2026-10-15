from models.Dbsystem import db
import time

"""

CREATE TABLE "products_item" (
	"itemid"	INTEGER,
	"name"	TEXT NOT NULL,
	"imgpath"	TEXT,
	"dimension "	TEXT NOT NULL,
	"material"	TEXT NOT NULL,
	"info"	TEXT,
	"addtime"	INTEGER NOT NULL,
	"lastUpdate"	INTEGER,
	"categoryid"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("itemid" AUTOINCREMENT),
	FOREIGN KEY("categoryid") REFERENCES "products_category"("categoryid")
);

"""

class Item(db.Model):    
    __tablename__ = "products_item"
    itemid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    imgpath = db.Column(db.String(100))
    dimension = db.Column(db.Text, nullable=False)
    material = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text)
    categoryid = db.Column(db.Integer, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default= lambda: int(time.time()))

    def __init__(self, name, imgPath, dimension, material, info, categoryId, addtime, lastUpdate):
        self.name = name
        self.imgpath = imgPath
        self.dimension = dimension
        self.material = material
        self.info = info
        self.categoryid = categoryId
        self.lastUpdate = lastUpdate
        self.addtime = addtime