from flask import Flask
from flask_cors import CORS
from reconstruction.api import reconstruction_api


app=Flask(__name__)
app.register_blueprint(reconstruction_api)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/hello',methods = ['GET'])
def get():
    return 'Hello From Modello Reconstruction Service'


if __name__=="__main__":
    app.run(host='0.0.0.0',port=FLASK_PORT,debug=True)


