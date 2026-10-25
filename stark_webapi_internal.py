from flask import Blueprint, request, jsonify, redirect, render_template
from PIL import Image
import os
import models.ModelList as model
from models.Dbsystem import db
import time
import hashlib
from datetime import datetime
# import json

internal_bp = Blueprint("internal_api", __name__)
# from flask import Flask
# dbName = "stark.db"

# internal_bp = Flask(__name__)
# internal_bp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# internal_bp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbName}"
# db.init_app(internal_bp)


@internal_bp.route("/internal/system/createalltables", methods=["POST"])
def CreateAllTables():
    db.create_all()
    msg = "Table Creation successful!"
    return msg

 
# banner
@internal_bp.route("/internal/index/banner", methods=["POST"])
def AddBanner():  
    imageName = datetime.now().strftime("%Y/%m/%d") +"_" + request.form.get('name')
    imageName = hashlib.sha256(imageName.encode("utf-8")).hexdigest()[:10]
    
    if request.files.get('image'):
        # 存入圖片        
        checkImg, imgPath = __SaveImage(request.files.get('image'), imageName, "banner")
        if not checkImg:
            msg = {"msg" : "image save failed!" }
            return jsonify(msg), 400
    else:
        imgPath = ""
    
    name = request.form.get('name')
    enable = True if request.form.get('enable') is not None and request.form.get('enable').lower() == "true" else False
    addtime = int(time.time())
    banner = model.Banner(name, imgPath, enable, addtime)
    db.session.add(banner)
    db.session.commit()
    return redirect("/backend/index/banner", code=303)


@internal_bp.route("/internal/index/banner", methods=["GET"])
def GetBanners():    
    query = model.Banner.query.filter_by(enable=1).all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
    }
    return jsonify(data), 200


@internal_bp.route("/internal/index/banner/<int:bannerId>", methods=["PUT"])
def SetBanner(bannerId):
    if bannerId < 0:
        msg = {"msg" : "bannerId is required" }
        return jsonify(msg), 400
    if not request.json.get('name') or request.json.get('name') == "":
        msg = {"msg" :"name is required" }
        return jsonify(msg), 400    
    if not request.json.get('enable') or request.json.get('enable') == "":
        msg = {"msg" :"enable is required" }
        return jsonify(msg), 400
    query = model.Banner.query.filter_by(bannerid=bannerId).first()
    query.name = request.json.get('name')
    query.enable = request.json.get('enable')
    db.session.commit()
    msg = {"msg" : "banner update successful!"}
    return jsonify(msg), 200  
 

@internal_bp.route("/internal/index/banner/<int:bannerId>", methods=["DELETE"])
def DeleteBanner(bannerId):    
    if bannerId < 0:
        msg = {"msg" : "bannerId is required" }
        return jsonify(msg), 400
    
    query = model.Banner.query.filter_by(bannerid=bannerId).first()
    # 刪除圖片
    checkFile = __DeleteFile(query.imgpath)
    if checkFile:
        db.session.delete(query)
        db.session.commit()
        msg = {"msg" : "banner delect succeful" }
        return jsonify(msg), 200
    else:
        msg = {"msg" : "image delete failed!" }
        return jsonify(msg), 400


# info
@internal_bp.route("/internal/index/info", methods=["POST"])
def AddInfo():
    if not request.form.get('title') or request.form.get('title') == "":
        msg = {"msg" : "title is required" }
        return jsonify(msg), 400
    
    count = len(model.Info.query.filter_by(title=request.form.get('title')).all())
    if count > 0:
        msg = {"msg" : "title is exists" }
        return jsonify(msg), 409
    
    imageName = datetime.now().strftime("%Y/%m/%d") +"_" +request.form.get('name')
    imageName = hashlib.sha256(imageName.encode("utf-8")).hexdigest()[:10]
    
    if request.files.get('image'):
        # 存入圖片        
        checkImg, imgPath = __SaveImage(request.files.get('image'), imageName, "info")
        if not checkImg:    
            msg = {"msg" : "image save failed!" }
            return jsonify(msg), 400
    else:
        imgPath = ""
    
    title = request.form.get('title') 
    enable = True if request.form.get('enable').lower() == "true" else False
    addtime = int(time.time())
    info = model.Info(title, imgPath, enable, addtime)
    db.session.add(info)
    db.session.commit()
    return redirect("/backend/index/info", code=303)


@internal_bp.route("/internal/index/info", methods=["GET"])
def GetInfos():    
    query = model.Info.query.filter_by(enable=1).all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200


@internal_bp.route("/internal/index/info/<int:infoId>", methods=["PUT"])
def SetInfo(infoId):
    if infoId < 0:
        msg = {"msg" : "infoId is required" }
        return jsonify(msg), 400
    
    if not request.json.get('title') or request.json.get('title') == "":
        msg = {"msg" : "title is required" }
        return jsonify(msg), 400
    
    if not request.json.get('enable') or request.json.get('enable') == "":
        msg = {"msg" :"enable is required"}
        return jsonify(msg), 400
    query = model.Info.query.filter_by(infoid=infoId).first()
    query.title = request.json.get('title')
    query.enable = request.json.get('enable')
    db.session.commit()
    msg = {"msg" : "info update successful!" }
    return jsonify(msg), 200

    
@internal_bp.route("/internal/index/info/<int:infoId>", methods=["DELETE"])
def DeleteInfo(infoId):    
    if infoId < -1:
        msg = {"msg": "infoId is required"}
        return jsonify(msg)
    
    query = model.Info.query.filter_by(infoid=infoId).first()
    # 刪除圖片
    checkFile = __DeleteFile(query.imgpath)
    if checkFile:
        db.session.delete(query)
        db.session.commit()
        msg = {"msg" : "info delect succeful" }
        return jsonify(msg), 200
    else:
        msg = {"msg" : "image delete failed!" }
        return jsonify(msg), 400


# history
@internal_bp.route("/internal/index/history", methods=["POST"])
def AddHistory():
    if not request.form.get('title') or request.form.get('title') == "":
        msg = {"msg" : "title is required"}
        return jsonify(msg), 400
    
    if not request.form.get('content') or request.form.get('content') == "":
        msg = {"msg" :"content is required"}
        return jsonify(msg), 400
    
    title = request.form.get('title') 
    content = request.form.get('content')
    addtime = int(time.time())
    lastUpdated = int(time.time())
    history = model.History(title, content, addtime, lastUpdated)
    db.session.add(history)
    db.session.commit()
    return redirect("/backend/index/history", code=303)

@internal_bp.route("/internal/index/history", methods=["GET"])
def GetHistorys():
    query = model.History.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/index/history/<int:historyId>", methods=["PUT"])
def SetHistory(historyId):
    if historyId < 0:
        msg = {"msg" : "historyId is required"}
        return jsonify(msg)
    
    if not request.json.get('title') or request.json.get('title') == "":
        msg = {"msg" : "title is required" }
        return jsonify(msg), 400
    
    if not request.json.get('content') or request.json.get('content') == "":
        msg = {"msg" : "content is required" }
        return jsonify(msg), 400
    
    query = model.History.query.filter_by(historyid=historyId).first()
    query.title = request.json.get('title')
    query.content = request.json.get('content')
    db.session.commit()
    msg = {"msg" : "history update successful!" }
    return jsonify(msg), 200
    
@internal_bp.route("/internal/index/history/<int:historyId>", methods=["DELETE"])
def DeleteHistory(historyId):
    if historyId < 0:
        msg = {"msg" : "historyId is required"}
        return jsonify(msg)
    
    query = model.History.query.filter_by(historyid=historyId).first()  
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "history delect succeful" }
    return jsonify(msg), 200


# features
# topic=1，專業技術文章；topic=2，產品品項文章
@internal_bp.route("/internal/features/featureInfo", methods=["POST"])
def AddFeatureInfo():
    if not request.form.get('topic'):
        msg = {"msg" : "topic is required" }
        return jsonify(msg), 400
        
    if not request.form.get('title') or request.form.get('title') == "":
        msg = {"msg" : "title is required" }
        return jsonify(msg), 400
    
    if not request.form.get('content') or request.form.get('content') == "":
        msg = {"msg" : "content is required" }
        return jsonify(msg), 400
    
    topic = request.form.get('topic')
    title = request.form.get('title')
    content = request.form.get('content')
    addtime = int(time.time())
    lastUpdated = int(time.time())
    features = model.FeatureInfo(topic, title, content, addtime, lastUpdated)
    db.session.add(features)
    db.session.commit()
    return redirect("/backend/features/featureInfo", code=303)

@internal_bp.route("/internal/features/featureInfo", methods=["GET"])
def GetFeatureInfo():
    query = model.FeatureInfo.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    query2 = model.FeatureType.query.filter_by(enable=1).all()
    query2 = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query2]
    data = {
        "data" : query,
        "topics" : query2
    }
    return jsonify(data), 200

@internal_bp.route("/internal/features/featureInfo/<int:topic>", methods=["GET"])
def GetFeatureInfoTopics(topic):
    if topic < 0:
        msg = {"msg" : "topic is required"}
        return jsonify(msg)
    query = model.FeatureInfo.query.filter_by(topic=topic).all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/features/featureInfo/<int:featureInfoId>", methods=["PUT"])
def SetFeatureInfo(featureInfoId):   
    if featureInfoId < 0:
        msg = {"msg" : "featureInfoId is required" }
        return jsonify(msg), 400
    
    if not request.json.get('topic') or request.json.get('topic') == "":
        msg = {"msg" : "topic is required" }
        return jsonify(msg), 400
    
    if not request.json.get('title') or request.json.get('title') == "":
        msg = {"msg" : "title is required" }
        return jsonify(msg), 400
    
    if not request.json.get('content') or request.json.get('content') == "":
        msg = {"msg" : "content is required" }
        return jsonify(msg), 400
    
    query = model.FeatureInfo.query.filter_by(featureinfoid=featureInfoId).first()
    query.topic = request.json.get('topic')
    query.title = request.json.get('title')
    query.content = request.json.get('content')
    db.session.commit()
    msg = {"msg" : "featureInfo update successful!" }
    return jsonify(msg), 200

@internal_bp.route("/internal/features/featureInfo/<int:featureInfoId>", methods=["DELETE"])
def DeleteFeatureInfo(featureInfoId):
    if not featureInfoId or featureInfoId == "":
        msg = {"msg" : "featureInfoId is required" }
        return jsonify(msg), 400
    
    query = model.FeatureInfo.query.filter_by(featureinfoid=featureInfoId).first()
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "featureInfo delete successful!" }
    return jsonify(msg), 200   


# topic=1，專業技術文章；topic=2，產品品項文章
@internal_bp.route("/internal/features/featureType", methods=["POST"])
def AddFeatureType():
    if not request.form.get('name') or request.form.get('name') == "":
        msg = {"msg" : "name is required" }
        print(msg)
        return jsonify(msg), 400
        
    if not request.form.get('chinese_name') or request.form.get('chinese_name') == "":
        msg = {"msg" : "chinese_name is required" }
        print(msg)
        return jsonify(msg), 400
    
    if request.form.get('enable') is None or request.form.get('enable') == "":
        msg = {"msg" : "enable is required" }
        print(msg)
        return jsonify(msg), 400
    
    name = request.form.get('name')
    chinese_name = request.form.get('chinese_name')
    enable = True if request.form.get('enable') is not None and request.form.get('enable').lower() == "true" else False
    featureType = model.FeatureType(name, chinese_name, enable)
    db.session.add(featureType)
    db.session.commit()
    return redirect("/backend/features/featureType", code=303)

@internal_bp.route("/internal/features/featureType", methods=["GET"])
def GetFeatureType():
    query = model.FeatureType.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/features/featureType/<int:featureTypeId>", methods=["GET"])
def GetFeatureTypeId(featureTypeId):
    query = model.FeatureType.filter_by(featuretypeid=featureTypeId).first()
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/features/featureType/<int:featureTypeId>", methods=["PUT"])
def SetfeatureType(featureTypeId):    
    if not featureTypeId or featureTypeId < 0:
        msg = {"msg" : "featureTypeId is required" }
        print(msg)
        return jsonify(msg), 400
    
    if not request.json.get('name') or request.json.get('name') == "":
        msg = {"msg" : "name is required" }
        print(msg)
        return jsonify(msg), 400
        
    if not request.json.get('chinese_name') or request.json.get('chinese_name') == "":
        msg = {"msg" : "chinese_name is required" }
        print(msg)
        return jsonify(msg), 400
    
    if request.json.get('enable') is None:
        msg = {"msg" : "enable is required" }
        print(msg)
        return jsonify(msg), 400
    
    query = model.FeatureType.query.filter_by(featuretypeid=featureTypeId).first()
    query.name = request.json.get('name')
    query.chinese_name = request.json.get('chinese_name')
    query.enable = True if request.json.get('enable') else False
    db.session.commit()
    msg = {"msg" : "featuresType update successful!" }
    return jsonify(msg), 200

@internal_bp.route("/internal/features/featureType/<int:featureTypeId>", methods=["DELETE"])
def DeleteFeatureType(featureTypeId):
    query = model.FeatureType.query.filter_by(featuretypeid=featureTypeId).first()
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "featuresType delete successful!" }
    return jsonify(msg), 200


# category
@internal_bp.route("/internal/product/category", methods=["POST"])
def AddCategory():
    if not request.form.get('name') or request.form.get('name') == "":
        msg = {"msg" : "name is required" }
        return jsonify(msg), 400
    
    name = request.form.get('name')
    enable = True if request.form.get('enable').lower() == "true" else False
    category = model.Category(name, enable)
    db.session.add(category)
    db.session.commit()
    return redirect("/backend/product/category", code=303)

@internal_bp.route("/internal/product/category", methods=["GET"])
def GetCategorys():
    query = model.Category.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/product/category/<int:categoryId>", methods=["PUT"])
def SetCategory(categoryId):
    if categoryId < -1:
        msg = {"msg" : "categoryId is required" }
        return jsonify(msg), 400
    
    if not request.json.get('name') or request.json.get('name') == "":
        msg = {"msg" : "name is required" }
        return jsonify(msg), 400
    
    if request.json.get('enable') is None or request.json.get('enable') == "":
        msg = {"msg" : "enable is required" }
        return jsonify(msg), 400
    
    query = model.Category.query.filter_by(categoryid=categoryId).first()
    query.name = request.json.get('name')
    query.enable = request.json.get('enable')
    db.session.commit()
    msg = {"msg" : "category update successful!" }
    return jsonify(msg), 200
    
@internal_bp.route("/internal/product/category/<int:categoryId>", methods=["DELETE"])
def DeleteCategory(categoryId):
    query = model.Category.query.filter_by(categoryid=categoryId).first()
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "category delete successful!" }
    return jsonify(msg), 200


# item
@internal_bp.route("/internal/product/item", methods=["POST"])
def AddItem():
    if not request.form.get('name') or request.form.get('name') == "":
        msg = {"msg" : "name is required" }
        return jsonify(msg), 400
    
    if not request.form.get('dimension') or request.form.get('dimension') == "":
        msg = {"msg" : "dimension is required" }
        return jsonify(msg), 400
    
    if not request.form.get('material') or request.form.get('material') == "":
        msg = {"msg" : "material is required" }
        return jsonify(msg), 400
    
    if not request.form.get('categoryid') or request.form.get('categoryid') == "":
        msg = {"msg" : "categoryid is required" }
        return jsonify(msg), 400
    
    if request.files.get('image'):
        # 存入圖片
        imageName = datetime.now().strftime("%Y/%m/%d") +"_" +request.form.get('name')
        imageName = hashlib.sha256(imageName.encode("utf-8")).hexdigest()[:10]
        checkImg, imgPath = __SaveImage(request.files.get('image'), imageName, "item")
        if not checkImg:
            msg = {"msg" : "image save failed!" }
            return jsonify(msg), 400       
    else:
        imgPath = ""
        
    name = request.form.get('name')
    dimension = request.form.get('dimension')
    material = request.form.get('material')
    info = request.form.get('info') if request.form.get('info') is not None else ""
    categoryId = request.form.get('categoryid')
    addtime = int(time.time())
    lastUpdated = int(time.time())
    item = model.Item(name, imgPath, dimension, material, info, categoryId, addtime, lastUpdated)
    db.session.add(item)
    db.session.commit()
    return redirect("/backend/product/item", code=303)

@internal_bp.route("/internal/product/item", methods=["GET"])
def GetItems():
    query = model.Item.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    query2 = model.Category.query.filter_by(enable=1).all()
    query2 = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query2]
    data = {
        "data" : query,
        "topics" : query2
    }
    return jsonify(data), 200

@internal_bp.route("/internal/product/item/<int:itemId>", methods=["GET"])
def GetItem(itemId):
    query = model.Item.query.filter_by(itemid=itemId).first()
    query = {k: v for k,v in query.__dict__.items() if k != '_sa_instance_state'}
    data = {
        "data" : query,
    }
    return jsonify(data), 200

@internal_bp.route("/internal/product/item/<int:itemId>", methods=["PUT"])
def SetItem(itemId):
    if itemId < -1:
        msg = {"msg" : "itemId is required" }
        return jsonify(msg), 400
    
    query = model.Item.query.filter_by(itemid=itemId).first()
    
    if request.form.get('name') and request.form.get('name') != "":
        query.name = request.form.get('name')

    if request.files.get('image'):
        if query.imgpath != "":
            # 刪除圖片
            checkImg = __DeleteFile(query.imgpath)
            if not checkImg:
                msg = {"msg" : "image delete failed!" }
                return jsonify(msg), 400
        # 存入圖片
        imageName = datetime.now().strftime("%Y/%m/%d") +"_" +request.form.get('name')
        imageName = hashlib.sha256(imageName.encode("utf-8")).hexdigest()[:10]
        checkImg, imgPath = __SaveImage(request.files.get('image'), imageName, "item")
        if not checkImg:
            query.imgpath = ""
            db.session.commit()
            msg = {"msg" : "image save failed!" }
            return jsonify(msg), 400
        
        query.imgpath = imgPath

    if request.form.get('dimension') and request.form.get('dimension') != "":
        query.dimension = request.form.get('dimension')
    
    if request.form.get('material') and request.form.get('material') != "":
        query.material = request.form.get('material')

    if request.form.get('info') and request.form.get('info') != "":
        query.info = request.form.get('info')
        
    if request.form.get('categoryid') and request.form.get('categoryid') != "":
        query.categoryid = request.form.get('categoryid')
    
    db.session.commit()
    msg = {"msg" : "item update successful!" }
    return jsonify(msg), 200

@internal_bp.route("/internal/product/item/<int:itemId>", methods=["DELETE"])
def DeleteItem(itemId):
    if itemId < -1:
        msg = {"msg" : "itemId is required" }
        return jsonify(msg), 400
    
    query = model.Item.query.filter_by(itemid=itemId).first()
    if query.imgpath != "":
        # 刪除圖片
        checkImg = __DeleteFile(query.imgpath)
        if not checkImg:
            msg = {"msg" : "image delete failed!"}
            return jsonify(msg), 400
    
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "item delete successful!"}
    return jsonify(msg), 200

# news
@internal_bp.route("/internal/news/news", methods=["POST"])
def AddNews():
    if request.form.get('title') is None or request.form.get('title') == "":
        msg = {"msg" : "title is required"}
        return jsonify(msg), 400
    
    if request.form.get('content') is None or request.form.get('content') == "":
        msg = {"msg" : "content is required"}
        return jsonify(msg), 400
    
    title = request.form.get('title')
    content = request.form.get('content')
    addtime = int(time.time())
    lastUpdate = int(time.time())
    news = model.News(title, content, addtime, lastUpdate)
    db.session.add(news)
    db.session.commit()
    return redirect("/backend/news/news", code=303)

@internal_bp.route("/internal/news/news", methods=["GET"])
def GetNewsList():
    query = model.News.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/news/news/<int:newsId>", methods=["GET"])
def GetNews(newsId):
    query = model.News.query.filter_by(newsid=newsId).first()
    query = {k: v for k,v in query.__dict__.items() if k != '_sa_instance_state'}
    data = {
        "data" : query
        }
    return jsonify(data), 200


@internal_bp.route("/internal/news/news/<int:newsId>", methods=["PUT"])
def SetNews(newsId):
    if newsId < 0:
        msg = {"msg" : "newsId is required"}
        return jsonify(msg), 400
    
    if not request.json.get('title') or request.json.get('title') == "":
        msg = {"msg" : "title is required"}
        return jsonify(msg), 400
    
    if not request.json.get('content') or request.json.get('content') == "":
        msg = {"msg" : "content is required"}
        return jsonify(msg), 400
    
    query = model.News.query.filter_by(newsid=newsId).first()
    query.title = request.json.get('title')
    query.content = request.json.get('content')     
    db.session.commit()
    msg = {"msg" : "news update successful!"}
    return jsonify(msg), 200


@internal_bp.route("/internal/news/news/<int:newsId>", methods=["DELETE"])
def DeleteNews(newsId):
    query = model.News.query.filter_by(newsid=newsId).first()
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "news delete successful!"}
    return jsonify(msg), 200
    

# faq
@internal_bp.route("/internal/faq/faq", methods=["POST"])
def AddFaq():
    if not request.form.get('question') or request.form.get('question') == "":
        msg = {"msg" : "question is required"}
        return jsonify(msg), 400
    
    if not request.form.get('answer') or request.form.get('answer') == "":
        msg = {"msg" : "answer is required"}
        return jsonify(msg), 400
    
    question = request.form.get('question')
    answer = request.form.get('answer')
    addtime = int(time.time())
    lastUpdate = int(time.time())
    faq = model.Faq(question, answer, addtime, lastUpdate)
    db.session.add(faq)
    db.session.commit()
    return redirect("/backend/faq/faq", code=303)

@internal_bp.route("/internal/faq/faq", methods=["GET"])
def GetFaqs():
    query = model.Faq.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/faq/faq/<int:faqId>", methods=["PUT"])
def SetFaq(faqId):
    if faqId < 0:
        msg = {"msg" : "faqId is required"}
        return jsonify(msg), 400
    
    if not request.json.get('question') or request.form.get('question') == "":
        msg = {"msg" : "question is required"}
        return jsonify(msg), 400
    
    if not request.json.get('answer') or request.form.get('answer') == "":
        msg = {"msg" : "answer is required"}
        return jsonify(msg), 400
    
    query = model.Faq.query.filter_by(faqid=faqId).first()
    query.question = request.json.get('question')
    query.answer = request.json.get('answer')     
    db.session.commit()
    msg = {"msg" : "faq update successful!"}
    return jsonify(msg), 200


@internal_bp.route("/internal/faq/faq/<int:faqId>", methods=["DELETE"])
def DeleteFaq(faqId):
    query = model.Faq.query.filter_by(faqid=faqId).first()
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "faq delete successful!"}
    return jsonify(msg), 200


# downloads
@internal_bp.route("/internal/downloads/downloads", methods=["POST"])
def AddDownloads():
    if request.form.get('name') is None or request.form.get('name') == "":
        msg = {"msg" : "name is required"}
        return jsonify(msg), 400   
        
    if request.form.get('version') is None or request.form.get('version') == "":
        msg = {"msg" : "version is required"}
        return jsonify(msg), 400
    
    
    if request.files.get('pdf') is not None:
        file = request.files.get('pdf')
        # 存入檔案    
        fileName = datetime.now().strftime("%Y/%m/%d") +"_" +request.form.get('name')
        fileName = hashlib.sha256(fileName.encode("utf-8")).hexdigest()[:10]
        print("雜湊完：" + fileName)
        checkFile, filePath = __SavePDF(request.files.get('pdf'), fileName)
        if not checkFile:
            msg = {"msg" : "file save failed!"}
            return jsonify(msg), 400
        
        size = __fileSize(file)
    else:
        filePath = ""
        size = ""
        
    name = request.form.get('name')
    
    version = request.form.get('version')
    info = request.form.get('info') if request.form.get('info') is not None else ""
    addtime = int(time.time())
    lastUpdate = int(time.time())
    downloads = model.Downloads(name, filePath, size, version, info, addtime, lastUpdate)
    db.session.add(downloads)
    db.session.commit()
    return redirect("/backend/downloads/downloads", code=303)

@internal_bp.route("/internal/downloads/downloads", methods=["GET"])
def GetDownloads():
    query = model.Downloads.query.all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
        }
    return jsonify(data), 200

@internal_bp.route("/internal/downloads/downloads/<int:downloadsId>", methods=["PUT"])
def SetDownloadsName(downloadsId):
    if downloadsId < 0:
        msg = {"msg" : "downloadsId is required"}
        return jsonify(msg), 400
    
    query = model.Downloads.query.filter_by(downloadsid=downloadsId).first()

    if request.form.get('name') and request.form.get('name') != "":
        query.name = request.form.get('name')

    if request.files.get('pdf'):
        file = request.files.get('pdf')
        if query.filepath != "":
            # 刪除圖片
            checkImg = __DeleteFile(query.filepath)
            if not checkImg:
                msg = {"msg" : "file delete failed!" }
                return jsonify(msg), 400
        # 存入圖片
        fileName = datetime.now().strftime("%Y/%m/%d") +"_" +request.form.get('name')
        fileName = hashlib.sha256(fileName.encode("utf-8")).hexdigest()[:10]
        checkFile, filePath = __SavePDF(request.files.get('pdf'), fileName)
        if not checkFile:
            query.imgpath = ""
            db.session.commit()
            msg = {"msg" : "file save failed!" }
            return jsonify(msg), 400
        query.filepath = filePath
        query.size = __fileSize(file)
    
    if request.form.get('version') and request.form.get('version') != "":
        query.version = request.form.get('version')
    
    if request.form.get('info') and request.form.get('info') != "":
        query.info = request.form.get('info')

    db.session.commit()
    msg = {"msg" : "downloads update successful!"}
    return jsonify(msg), 200

@internal_bp.route("/internal/downloads/downloads/<int:downloadsId>", methods=["DELETE"])
def DeleteDownloads(downloadsId):
    query = model.Downloads.query.filter_by(downloadsid=downloadsId).first()
    if query.filepath != "":
        # 刪除PDF
        checkFile = __DeleteFile(query.filepath)
        if not checkFile:
            msg = {"msg" : "PDF delete failed!"}
            return jsonify(msg), 400
    
    db.session.delete(query)
    db.session.commit()
    msg = {"msg" : "downloads delete successful!"}
    return jsonify(msg), 200

# company
@internal_bp.route("/internal/contactUs/company", methods=["POST"])
def AddCompany():
    if model.Company.query.first() is not None:
        msg = {"msg" : "company is exists"}
        return jsonify(msg), 400
    
    if request.form.get('name') is None or request.form.get('name') == "":
        msg = {"msg" : "name is required"}
        return jsonify(msg), 400
    
    if request.form.get('email') is None or request.form.get('email') == "":
        msg = {"msg" : "email is required"}
        return jsonify(msg), 400
    
    if request.form.get('address') is None or request.form.get('address') == "":
        msg = {"msg" : "address is required"}
        return jsonify(msg), 400
    
    if request.form.get('phone') is None or request.form.get('phone') == "":
        msg = {"msg" : "phone is required"}
        return jsonify(msg), 400

    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    phone = request.form.get('phone')
    fax = request.form.get('fax')
    servicetime = request.form.get('servicetime')
    company = model.Company(name, email, address, phone, fax, servicetime)
    db.session.add(company)
    db.session.commit()
    return redirect("/backend/contactUs/company", code=303)

@internal_bp.route("/internal/contactUs/company", methods=["GET"])
def GetCompany():    
    query = model.Company.query.first()
    query = {k: v for k,v in query.__dict__.items() if k != '_sa_instance_state'}
    data = {
        "data" : query
        }    
    return jsonify(data), 200

@internal_bp.route("/internal/contactUs/company", methods=["PUT"])
def SetCompany():
    query = model.Company.query.first()
    if request.json.get('name') and request.json.get('name') != "":
        query.name = request.json.get('name')
    
    if request.json.get('email') and request.json.get('email') != "":
        query.email = request.json.get('email')
    
    if request.json.get('address') and request.json.get('address') != "":
        query.address = request.json.get('address')
    
    if request.json.get('phone') and request.form.get('phone') != "":
        query.phone = request.json.get('phone')
    
    if request.json.get('fax') and request.json.get('fax') != "":
        query.fax = request.json.get('fax')
    
    if request.json.get('servicetime') and request.form.get('servicetime') != "":
        query.servicetime = request.json.get('servicetime')
    
    db.session.commit()
    msg = {"msg" : "Company update successful!"}
    return jsonify(msg), 200

# form
@internal_bp.route("/internal/contactUs/form", methods=["POST"])
def AddForm():    
    if request.form.get('contactname') is None or request.form.get('contactname') == "":
        msg = {"msg" : "contactname is required"}
        return jsonify(msg), 400
    
    if request.form.get('address') is None or request.form.get('address') == "":
        msg = {"msg" : "address is required"}
        return jsonify(msg), 400
    
    if request.form.get('phone') is None or request.form.get('phone') == "":
        msg = {"msg" : "phone is required"}
        return jsonify(msg), 400
    
    if request.form.get('email') is None or request.form.get('email') == "":
        msg = {"msg" : "email is required"}
        return jsonify(msg), 400
    
    if request.form.get('title') is None or request.form.get('title') == "":
        msg = {"msg" : "title is required"}
        return jsonify(msg), 400
    
    if request.form.get('content') is None or request.form.get('content') == "":
        msg = {"msg" : "content is required"}
        return jsonify(msg), 400

    companyname = request.form.get('companyname') if request.form.get('companyname') is not None else ""
    contactname = request.form.get('contactname')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    title = request.form.get('title')
    content = request.form.get('content')
    addtime = int(time.time())
    form = model.Form(companyname, contactname, address, phone, email, title, content, addtime)
    db.session.add(form)
    db.session.commit()
    checkAddMessage = AddMessage()
    if not checkAddMessage:
        db.session.delete(form)
        db.session.commit()
        msg = "form insert failed!"
        return jsonify(msg), 400
    msg = "banner update successful!"
    return render_template("front_contactus.htm", msg=msg)


@internal_bp.route("/internal/contactUs/form/<formId>", methods=["GET"])
def GetForm(formId):
    query = model.Form.query.filter_by(formid=formId).first()
    query = {k: v for k,v in query.__dict__.items() if k != '_sa_instance_state'}
    data = {
        "data" : query
        }
    return jsonify(data), 200


# message
def AddMessage():
    checkAddMessage = False
    query = model.Form.query.order_by(model.Form.addtime.desc()).first()
    if (query == None):        
        return checkAddMessage
    formid = query.formid
    read = False
    processed = False
    lastUpdate = int(time.time())
    form = model.Message(formid, read, processed, lastUpdate)
    db.session.add(form)
    db.session.commit()
    checkAddMessage = True
    return checkAddMessage

@internal_bp.route("/internal/contactUs/message", methods=["GET"])
def GetMessages():    
    query = model.Message.query.order_by(model.Message.processed.asc(), model.Message.read.asc(), model.Message.lastUpdate.desc()).all()
    query = [{k: v for k,v in item.__dict__.items() if k != '_sa_instance_state'} for item in query]
    data = {
        "data" : query
    }
    return jsonify(data), 200

@internal_bp.route("/internal/contactUs/message/read/<int:messageId>", methods=["PUT"])
def SetMessageRead(messageId):    
    query = model.Message.query.filter_by(messageid=messageId).first()
    query.read = True
    db.session.commit()    
    return jsonify(), 200
    
@internal_bp.route("/internal/contactUs/message/processed/<int:messageId>", methods=["PUT"])
def SetMessageProcessed(messageId):
    query = model.Message.query.filter_by(messageid=messageId).first()
    query.processed = request.json.get('processed')      
    db.session.commit()
    msg = {
        "msg" : "message update successful!"
    }
    return jsonify(msg), 200



def __fileSize(file):
    sizeType = ["B", "KB", "MB", "GB"]
    index = 0
    file.seek(0)
    file.seek(0, 2)
    sizeNumber = file.tell()
    while (sizeNumber >= 1024):
        index = index + 1
        sizeNumber = sizeNumber / 1024
    size = f"{sizeNumber:.2f} {sizeType[index]}"
    return size

def __SaveImage(img, name: str, imgType: str):
    try:
        filePath = ""
        checkImg = False
        if img is None:
            raise Exception()      
        with Image.open(img.stream) as imgFile:
            imgFile.verify()            
        img.stream.seek(0)
        imgFile = Image.open(img.stream)
        
        filePath = os.path.join("static", "img", imgType)
        if(not os.path.exists(filePath)):
            os.makedirs(filePath)
        filePath = os.path.join(filePath, f"{name}.webp")        
        imgFile.save(filePath, "WEBP",lossless=True)
        filePath = os.path.join("\\", filePath)
        filePath = filePath.replace("\\", "/")
        checkImg = True
    except Exception as e:
        print(f"圖片儲存失敗，原因: {e}")
        checkImg = False
   
    return checkImg, filePath

def __SavePDF(file, name: str):
    try:
        filePath = ""
        if file is None:
            raise Exception()   
            
        filePath = os.path.join("static", "pdf")
        if(not os.path.exists(filePath)):
            os.makedirs(filePath)
        filePath = os.path.join(filePath, f"{name}.pdf")
        file.save(filePath)
        filePath = os.path.join("\\", filePath)
        filePath = filePath.replace("\\", "/")
        print("儲存完："+ filePath)
        checkFile = True
    except:
        checkFile = False
    finally:
        return checkFile, filePath
    
def __DeleteFile(filePath: str):
    filePath = filePath[1:]
    print("刪除檔案")
    print('目前目錄：', os.getcwd())
    print('檔案路徑：', os.path.abspath(filePath))
    if (os.path.exists(filePath)):    
        print("路徑正確")
        os.remove(filePath)
        checkFile = True
        print("刪除成功")
    else:
        checkFile = False
        print("刪除失敗")
    return checkFile

   
    
    
if __name__ == "__main__":    
    internal_bp.run(debug=True)
