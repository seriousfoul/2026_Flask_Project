from flask import render_template,Blueprint
from models.Dbsystem import db
from stark_webapi_internal import internal_bp as internal
import json
import requests


backend_bp = Blueprint("backend_api",__name__)
# from flask import Flask
# dbName = "stark.db"
ip = "127.0.0.1"
port = "5000"


# backend_bp = Flask(__name__)
# backend_bp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# backend_bp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbName}"
# backend_bp.register_blueprint(internal)
# db.init_app(backend_bp)


pageTypeName = {
    "index":"首頁設定",
    "features":"核心特色",
    "product":"產品相關",
    "news":"最新消息",
    "faq":"常見問題",
    "downloads":"文件下載",
    "contactUs":"聯絡我們",
    "banner":"首頁橫幅",
    "info":"公司照片",
    "history": "歷史前沿",
    "featureType": "特色種類",
    "featureInfo": "特色資訊",
    "category":"產品種類",
    "item":"產品資訊",
    "company":"公司資訊",
    "form":"諮詢表單",
    "message":"訊息通知"
    }

pageMainType = [
    "index", 
    "features", 
    "product", 
    "news", 
    "faq", 
    "downloads", 
    "contactUs" 
    ]

pageSubType = {
    "index" : ["banner", "info", "history"],
    "features": ["featureType", "featureInfo"],
    "product": ["category", "item"],
    "news": ["news"],
    "faq": ["faq"],
    "downloads": ["downloads"],
    "contactUs": ["company", "message"]
    }

typeData = {}
for mainType in pageMainType:   
    typeData[mainType] = pageTypeName.get(mainType)

subTypeData = {}
for typeName, subTypeList in pageSubType.items():
    subType = []
    for subTypeName in subTypeList:
        subType.append({
               "type": subTypeName,
               "typeName": pageTypeName.get(subTypeName)
            })
    subTypeData[typeName] = subType


# 後端
@backend_bp.route("/backend")
def BackendTemplate():
    msg = ""
    if "banner" not in db.metadata.tables:
        data = requests.post(f"http://{ip}:{port}/internal/system/createalltables")
        data.encoding = "utf-8"
        msg = data.text    
    return render_template("backend_template.htm", menu=typeData, msg=msg)

@backend_bp.route("/backend/<pageMain>")
def BackendPageMain(pageMain):
    if not pageMain and pageMain not in pageMainType:
        msg = "main type is error"
        return render_template("backend_template.htm", msg=msg)
        
    pageSub = pageSubType.get(pageMain)[0]
    respone = requests.get(f"http://{ip}:{port}/internal/{pageMain}/{pageSub}")
    data = respone.json()
    menu = subTypeData.get(pageMain) 
    return render_template(f"backend_{pageSub}.htm", subMenu=menu, mainType=pageMain, subType=pageSub, data=data.get("data"), msg=data.get("msg"), topics=data.get("topics"))
    

@backend_bp.route("/backend/<pageMain>/<pageSub>")
def BackendPageSub(pageMain, pageSub):
    if not pageMain and pageMain not in pageMainType:
        msg = "main type is error"
        return render_template("backend_template.htm", msg=msg)
    if not pageSub and pageSub not in pageSubType.get(pageMain):
        msg = "sub type is error"
        return render_template("backend_template.htm", msg=msg)
    respone = requests.get(f"http://{ip}:{port}/internal/{pageMain}/{pageSub}")
    data = respone.json()
    menu = subTypeData.get(pageMain)
    return render_template(f"backend_{pageSub}.htm", subMenu=menu, mainType=pageMain, subType=pageSub, data=data.get("data"), msg=data.get("msg"), topics=data.get("topics"))

if __name__ == "__main__":
    backend_bp.run()
