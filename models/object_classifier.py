from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os

class Object_Predicter():
	def __init__(self):
		app = ClarifaiApp(api_key='8bf951876b164091909b8c3f54bd642f')
		self.model = app.models.get('general-v1.3')
	def predict(self, link):
		image = ClImage(file_obj=open(link, 'rb'))
		response = self.model.predict([image])
		concepts = response['outputs'][0]['data']['concepts']
		for concept in concepts:
		    print(concept['name'], concept['value'])

if __name__ == "__main__":
	classifier = Object_Predicter()
	path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../static/img/hi.jpg')
	classifier.predict(path)