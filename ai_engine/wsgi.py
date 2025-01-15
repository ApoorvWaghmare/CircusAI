from flask import Flask
from flask_cors import CORS

#----------#

from config import DevelopmentConfig
from app_ai.services import StartUpService
from app_ai.routes import ai_app_bp

#------------------------------------------------------------------------------------------------------------------#

app = Flask(__name__) # on the terminal type: curl http://127.0.0.1:5000/ 
CORS(app) # Enable CORS for all routes in the Flask app
app.config.from_object(DevelopmentConfig)
app.register_blueprint(ai_app_bp, url_prefix = '/ai_engine/app')

#------------------------------------------------------------------------------------------------------------------#

StartUpService.initialize_model_management_service()

#------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run()