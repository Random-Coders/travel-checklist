from flask import Flask, render_template, request, make_response, redirect
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from json import load, dump # parse and add json data

app = Flask(__name__, template_folder='templates')

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'checklist' in request.cookies:
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename
        return render_template('upload.html')
    else:
        return redirect("/yourchecklist", code=302)

temppath = os.getcwd()

@app.route('/yourchecklist', methods=['GET'])
def checklist():
    if 'checklist' in request.cookies:
        checklist_name = request.cookies['checklist']
        with open(temppath + '/data/lists.json', 'r') as list_data:
            list_data = load(list_data)
        list = list_data[checklist_name]['data']
        return render_template('checklist.html', list=list)
    else:
        res = make_response(render_template('checklist.html', list='None'))
        with open(temppath + '/data/lists.json', 'r') as contact_data:
            lists_exists = load(contact_data) # read data
        ur_key = os.urandom(30)
        with open(temppath + '/data/lists.json', 'w') as outfile:
                lists_exists['lists'][str(ur_key)] = {'data':'None'} # new data to add
                dump(lists_exists, outfile) # add data
        res.set_cookie('checklist', ur_key, max_age=60*60*24*365)
        return res

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
