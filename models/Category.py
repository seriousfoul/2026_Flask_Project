from models.Dbsystem import db

"""

CREATE TABLE "products_category" (
	"categoryid"	INTEGER,
	"name"	TEXT NOT NULL,
	"enable"	INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY("categoryid" AUTOINCREMENT)
);

"""

class Category(db.Model):    
    __tablename__ = "products_category"
    categoryid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    enable = db.Column(db.Boolean, default=True)
    
    def __init__(self, name, enable):
        self.name = name
        self.enable = enable