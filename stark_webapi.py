from flask import Flask
from models.Dbsystem import db
from stark_webapi_internal import internal_bp as internal
from stark_webapi_backend import backend_bp as backend
from stark_webapi_front import front_bp as front


dbName = "stark.db"
ip = "127.0.0.1"
port = "5000"

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbName}"
app.register_blueprint(internal)
app.register_blueprint(backend)
app.register_blueprint(front)

db.init_app(app)



if __name__ == "__main__":
    app.run()
