from models.Dbsystem import db

"""

CREATE TABLE "feature_type" (
	"featuretypeid"	INTEGER,
	"name"	TEXT NOT NULL,
    "chinese_name" TEXT NOT NULL
	"enable" BOOLEAN Dafault 1,
	PRIMARY KEY("featuresid" AUTOINCREMENT)
);

"""

class FeatureType(db.Model):    
    __tablename__ = "feature_type"
    featuretypeid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    chinese_name = db.Column(db.String(30), nullable=False)
    enable = db.Column(db.Integer, default= 1, nullable=False)

    def __init__(self, name, chinese_name, enable):
        self.name = name
        self.chinese_name = chinese_name
        self.enable = enable