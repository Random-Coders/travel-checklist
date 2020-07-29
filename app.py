from flask import Flask, render_template, request, make_response, redirect, url_for
#from models.object_classifier import Object_Predicter # Not used for post-hackathon example site
#import os
#from json import load, dump  # parse and add json data
#from base64 import b64encode

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload():

    # cookies
    if 'checklist' in request.cookies:
        #user_chosen_object = request.form.getlist('option')

        # if we have a user given value
        '''
        if len(user_chosen_object) != 0:

            checklist_name = request.cookies['checklist']
            with open(temppath + '/data/lists.json', 'r') as list_data:
                list_data = load(list_data)
                list_data["lists"][checklist_name]["list"].append(
                    user_chosen_object[0])

            if list_data["lists"][checklist_name]["data"] == 'None':
                list_data["lists"][checklist_name]["data"] = user_chosen_object[0]

            else:
                list_data["lists"][checklist_name]["data"] += user_chosen_object[0]

            with open(temppath + '/data/lists.json', 'w') as outfile:
                dump(list_data, outfile, separators=(',', ':'))  # add data
        '''

        # check if it is the right method
        if request.method == 'POST':# and 'photo' in request.files:
            '''
            # get the photo
            filename = photos.save(request.files['photo'])
            # init the predicter
            classifier = Object_Predicter()
            # predict given image
            classifier.predict(
                os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    f'static/img/{filename}'))
            # retrieve the concepts
            response = classifier.get_top_concepts(4)
            # remove it since we no longer need it
            os.remove(
                os.path.join(
                    os.path.dirname(
                        os.path.realpath(__file__)),
                    f'static/img/{filename}'))
            # return the results
            return render_template(
                'upload_more.html', options=[
                    concept[0] for concept in response])
            '''
            return redirect(url_for('checklist'))
        # if there is no file to upload
        return render_template('upload.html')
    else:
        return redirect(url_for('checklist'))


@app.route('/checklist', methods=['GET'])
@app.route('/yourchecklist', methods=['GET'])
def checklist():
    '''
    if 'checklist' in request.cookies:
        checklist_name = request.cookies['checklist']
        with open(temppath + '/data/lists.json', 'r') as list_data:
            list_data = load(list_data)
        list = list_data['lists'][checklist_name]['list']
        if list == 'None':
            return render_template('checklist-2.html')
        else:
            list_html = list
            print(list_html)
            print("list html", list_html)
            return render_template('checklist.html', list=list_html)
    else:
        res = make_response(render_template('checklist.html', list='None'))
        with open(temppath + '/data/lists.json', 'r') as contact_data:
            lists_exists = load(contact_data)  # read data
        ur_key = os.urandom(64)
        token = b64encode(ur_key).decode('utf-8')
        with open(temppath + '/data/lists.json', 'w') as outfile:
            lists_exists['lists'][str(token)] = {'data': 'None', 'list': [
            ], 'status': 'home'}  # new data to add
            dump(lists_exists, outfile, separators=(',', ':'))  # add data
        res.set_cookie('checklist', str(token), max_age=60 * 60 * 24 * 365)
        return res
    '''
    exampleList = ['Sandals', 'Rayban Sunglasses', 'Beach Towel', '5 pairs of socks', 'Sunblock', 'Loation', 'Day Pack']
    return render_template('checklist.html', list=exampleList)


@app.route('/', methods=['GET'])
def home():
    if 'once' in request.cookies:
        res = make_response(render_template('index.html'))
        res.set_cookie('alert', 'alerted', max_age=60 * 60 * 24 * 365)
        return res
    elif 'alert' in request.cookies:
        return render_template('index.html')
    else:
        res = make_response(render_template('index.html'))
        res.set_cookie('once', 'ran', max_age=60 * 60 * 24 * 365)
        return res


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
