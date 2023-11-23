from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
from config import *



app=Flask(__name__)

config_class = {
    'production': ProductionConfig,
    'testing': TestingConfig,
}.get(app.config.get('FLASK_ENV', 'development'), DevelopmentConfig)

app.config.from_object(config_class)

app.register_blueprint(api_bp)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/',methods = ['GET'])
def get():
    return 'Hello From Modello Reconstruction Service'


if __name__=="__main__":
    app.run(host='0.0.0.0',port=app.config['FLASK_PORT'])


