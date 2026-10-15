from flask import render_template, Blueprint, redirect
# from models.Dbsystem import db
# from stark_webapi_internal import internal_bp as internal
import requests
import json
import random

front_bp = Blueprint("front_api",__name__)
# from flask import Flask
# dbName = "stark.db"
ip = "127.0.0.1"
port = "5000"


# front_bp = Flask(__name__)
# front_bp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# front_bp.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbName}"
# front_bp.register_blueprint(internal)
# db.init_app(front_bp)


# 前端
@front_bp.route("/")
def root():
    respone = requests.get(f"http://{ip}:{port}/internal/features/featureInfo/3")
    brandSlogan = json.loads(respone.text)['data']
    brandSlogan = brandSlogan[random.randint(0, len(brandSlogan)-1)]['content']
    
    respone = requests.get(f"http://{ip}:{port}/internal/contactUs/company")
    company = json.loads(respone.text)['data']
    return render_template("front_template.htm", **locals())

# 首頁
@front_bp.route("/index")
def Index():
    respone = requests.get(f"http://{ip}:{port}/internal/index/banner")
    banner = json.loads(respone.text)['data']
    respone = requests.get(f"http://{ip}:{port}/internal/index/history")
    history = json.loads(respone.text)['data']
    respone = requests.get(f"http://{ip}:{port}/internal/index/info")
    info = json.loads(respone.text)['data']
    respone = requests.get(f"http://{ip}:{port}/internal/news/news")
    news = json.loads(respone.text)['data']
    news = sorted(news[-3:], key=lambda x:-x['lastUpdate'])
    return render_template("front_home.htm", **locals())

# 產品特色
@front_bp.route("/features")
def Features():
    respone = requests.get(f"http://{ip}:{port}/internal/features/featureInfo")
    features = json.loads(respone.text)['data']
    topics = json.loads(respone.text)['topics']
    return render_template("front_feature.htm", **locals()) 

# 產品介紹
@front_bp.route("/products")
def Products():
    respone = requests.get(f"http://{ip}:{port}/internal/product/item")
    products = json.loads(respone.text)['data']
    topics = json.loads(respone.text)['topics']
    return render_template("front_product.htm", **locals()) 

@front_bp.route("/products/productInfo/<int:productId>")
def ProductInfo(productId):
    respone = requests.get(f"http://{ip}:{port}/internal/product/item/{productId}")
    product = json.loads(respone.text)['data']
    product['dimension'] = product['dimension'].replace("{","").replace("}","")
    product['info'] = product['info'].replace("{","").replace("}","")
    return render_template("front_productInfo.htm", **locals()) 

# 最新消息
@front_bp.route("/news")
def News():
    respone = requests.get(f"http://{ip}:{port}/internal/news/news")
    news = json.loads(respone.text)['data']
    news = sorted(news, key=lambda x:-x['lastUpdate'])
    return render_template("front_news.htm", **locals())

@front_bp.route("/news/newsinfo/<int:id>")
def NewsInfo(id):
    respone = requests.get(f"http://{ip}:{port}/internal/news/news/{id}")
    news = json.loads(respone.text)['data']   
    return render_template("front_newsInfo.htm", **locals())


# 常見問題
@front_bp.route("/faq")
def FAQ():
    respone = requests.get(f"http://{ip}:{port}/internal/faq/faq")
    respone = json.loads(respone.text)
    return render_template("front_faq.htm", data=respone['data'])


# 目錄下載(型錄/技術文件) 
@front_bp.route("/downloads")
def Downloads():
    respone = requests.get(f"http://{ip}:{port}/internal/downloads/downloads")
    respone = json.loads(respone.text)
    return render_template("front_downloads.htm", data=respone['data'])

# 聯絡我們
@front_bp.route("/contactus")
def ContactUs():
    return render_template("front_contactus.htm")


if __name__ == "__main__":
    front_bp.run()
