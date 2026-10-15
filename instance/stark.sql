BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "contactus_company" (
	"name"	VARCHAR(30) NOT NULL,
	"email"	VARCHAR(100) NOT NULL,
	"address"	VARCHAR(100) NOT NULL,
	"phone"	VARCHAR(20) NOT NULL,
	"fax"	VARCHAR(20),
	"servicetime"	TEXT,
	PRIMARY KEY("name")
);
CREATE TABLE IF NOT EXISTS "contactus_form" (
	"formid"	INTEGER NOT NULL,
	"companyname"	VARCHAR(30),
	"contactname"	VARCHAR(10) NOT NULL,
	"email"	VARCHAR(100) NOT NULL,
	"address"	VARCHAR(100) NOT NULL,
	"phone"	VARCHAR(20) NOT NULL,
	"title"	VARCHAR(30) NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER,
	PRIMARY KEY("formid")
);
CREATE TABLE IF NOT EXISTS "contactus_message" (
	"messageid"	INTEGER NOT NULL,
	"formid"	INTEGER NOT NULL,
	"read"	BOOLEAN,
	"processed"	BOOLEAN,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("messageid")
);
CREATE TABLE IF NOT EXISTS "downloads" (
	"downloadsid"	INTEGER NOT NULL,
	"name"	VARCHAR(30) NOT NULL,
	"filepath"	VARCHAR(100) NOT NULL,
	"size"	VARCHAR(30) NOT NULL,
	"version"	VARCHAR(30) NOT NULL,
	"info"	TEXT,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("downloadsid")
);
CREATE TABLE IF NOT EXISTS "faq" (
	"faqid"	INTEGER NOT NULL,
	"question"	VARCHAR(200) NOT NULL,
	"answer"	TEXT NOT NULL,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("faqid")
);
CREATE TABLE IF NOT EXISTS "feature_info" (
	"featureinfoid"	INTEGER NOT NULL,
	"topic"	INTEGER,
	"title"	TEXT NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("featureinfoid")
);
CREATE TABLE IF NOT EXISTS "feature_type" (
	"featuretypeid"	INTEGER,
	"name"	TEXT NOT NULL,
	"chinese_name"	INTEGER NOT NULL,
	"enable"	BOOLEAN DEFAULT 1,
	PRIMARY KEY("featuretypeid" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "homepage_banner" (
	"bannerid"	INTEGER NOT NULL,
	"name"	VARCHAR(30),
	"imgpath"	VARCHAR(100) NOT NULL,
	"enable"	BOOLEAN,
	"addtime"	INTEGER,
	PRIMARY KEY("bannerid")
);
CREATE TABLE IF NOT EXISTS "homepage_history" (
	"historyid"	INTEGER NOT NULL,
	"title"	VARCHAR(30) NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("historyid")
);
CREATE TABLE IF NOT EXISTS "homepage_info" (
	"infoid"	INTEGER NOT NULL,
	"title"	VARCHAR(30) NOT NULL,
	"imgpath"	VARCHAR(100) NOT NULL,
	"enable"	BOOLEAN,
	"addtime"	INTEGER,
	PRIMARY KEY("infoid")
);
CREATE TABLE IF NOT EXISTS "news" (
	"newsid"	INTEGER NOT NULL,
	"title"	VARCHAR(30) NOT NULL,
	"content"	TEXT NOT NULL,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("newsid")
);
CREATE TABLE IF NOT EXISTS "products_category" (
	"categoryid"	INTEGER NOT NULL,
	"name"	VARCHAR(30) NOT NULL,
	"enable"	BOOLEAN,
	PRIMARY KEY("categoryid")
);
CREATE TABLE IF NOT EXISTS "products_item" (
	"itemid"	INTEGER NOT NULL,
	"name"	VARCHAR(30) NOT NULL,
	"imgpath"	VARCHAR(100),
	"dimension"	TEXT NOT NULL,
	"material"	VARCHAR(100) NOT NULL,
	"info"	TEXT,
	"categoryid"	INTEGER NOT NULL,
	"addtime"	INTEGER,
	"lastUpdate"	INTEGER,
	PRIMARY KEY("itemid")
);
COMMIT;
