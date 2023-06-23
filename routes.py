from flask import Blueprint, jsonify, request, render_template
#testasdasfasfa
routes = Blueprint('routes', __name__, template_folder='templates')

uploadedImages = {}
segmentedImages = {}

@routes.route("/")
def main():
    return render_template('index.html')

@routes.route('/api/loadImage', methods = ['GET'])
def load_image():
    file = request.json()
    print(file)
    return 

@routes.route('/api/saveImage', methods = ['POST'])
def save_image():
    file = request.json()
    print(file)
    return jsonify()

@routes.route('/api/segmentImage', methods = ['POST'])
def segment_image():
    file = request.json()
    print(file)
    return jsonify()