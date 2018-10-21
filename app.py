from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from models.object_classifier import Object_Predicter
import os

app = Flask(__name__, template_folder='templates')

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	# check if it is the right method
    if request.method == 'POST' and 'photo' in request.files:
    	# get the photo
        filename = photos.save(request.files['photo'])
        # init the predicter
        classifier = Object_Predicter()
        # predict given image
        classifier.predict(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'static/img/{filename}'))
        # retrieve the concepts
        response = classifier.get_concepts()
        # remove it since we no longer need it
        os.remove(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'static/img/{filename}'))
        # return the results
        return ', '.join([f"{concept[0]}{concept[1]}" for concept in response])
    return render_template('upload.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
