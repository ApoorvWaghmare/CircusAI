from flask import request, jsonify, Blueprint
from werkzeug.exceptions import BadRequest

#----------#

from .services import Text2ImageService, TextImage2ImageService

#----------#

ai_app_bp = Blueprint('ai_engine', __name__)

#------------------------------------------------------------------------------------------------------------------#

@ai_app_bp.route('/text-2-image', methods = ['GET'])
def text_2_image():
    try:
        prompt = request.args.get('prompt')

        if not prompt:
            raise BadRequest("Prompt is required.")
        
        return Text2ImageService.process(prompt = prompt), 202
    
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    
#------------------------------------------------------------------------------------------------------------------#

@ai_app_bp.route('text-image-2-image', methods = ['GET'])
def text_image_2_image():
    try:
        prompted_media_ref = request.args.get('prompted_media_ref')
        prompt = request.args.get('prompt')
        print("inside text_image_2_image")
        print(prompted_media_ref)
        print(prompt)

        if (not prompted_media_ref):
            raise BadRequest("Prompted_media_ref required.")
        if (not prompt):
            raise BadRequest("Prompt required.")
        
        return TextImage2ImageService.process(prompted_media_ref = prompted_media_ref, prompt = prompt), 200
    
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500