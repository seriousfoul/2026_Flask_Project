from models.Dbsystem import db
import time

"""

CREATE TABLE "features" (
	"featuresid"	INTEGER,
	"topic"	INTEGER NOT NULL DEFAULT 1,
	"content"	TEXT,
	"addtime"	INTEGER NOT NULL,
	"update"	INTEGER,
	PRIMARY KEY("featuresid" AUTOINCREMENT)
);

"""

class FeatureInfo(db.Model):    
    __tablename__ = "feature_info"
    featureinfoid = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Integer, default=1)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    addtime = db.Column(db.Integer, default= lambda: int(time.time()))
    lastUpdate = db.Column(db.Integer, onupdate=lambda: int(time.time()), default= lambda: int(time.time()))

    def __init__(self, topic, title, content, addtime, lastUpdate):
        self.topic = topic
        self.title = title
        self.content = content
        self.addtime = addtime
        self.lastUpdate = lastUpdate