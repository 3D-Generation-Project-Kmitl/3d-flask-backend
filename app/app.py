from flask import Flask
from flask_cors import CORS
from api.routes import api_bp


app=Flask(__name__)

if app.config['FLASK_ENV']=='production':
    app.config.from_object('config.ProductionConfig')
elif app.config['FLASK_ENV']=='testing':
    app.config.from_object('config.TestingConfig')
else:    
    app.config.from_object('config.DevelopmentConfig')

app.register_blueprint(api_bp)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/hello',methods = ['GET'])
def get():
    return 'Hello From Modello Reconstruction Service'


if __name__=="__main__":
    app.run(host='0.0.0.0',port=app.config['FLASK_PORT'])


