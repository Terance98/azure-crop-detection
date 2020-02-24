from flask import Flask, redirect, url_for, request
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import requests
from array import array
import os
from PIL import Image
import sys
import time
from pymongo import MongoClient
import json


# client = MongoClient()
client = MongoClient('mongodb://localhost:27017')

db = client.beachhack2


os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = "your-api-key"
subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']

os.environ['COMPUTER_VISION_ENDPOINT'] = "your-end-point"
endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

app = Flask(__name__)

#Fruits array
fruitsArray = ['orange', 'apple', 'banana', 'jackfruit', 'grape', 'lemon']

@app.route('/',methods = ['POST', 'GET'])
def login():
   cropDetails = []
   if request.method == 'POST':
      url = request.form['url']
   else:
      url = request.args.get('url')

   remote_image_url = url
   print("===== Describe an image - remote =====")
	# Call API
   description_results = computervision_client.describe_image(remote_image_url )

   tags_array = description_results.tags
   final_tags_array = list(filter(lambda fruit: fruit in fruitsArray, tags_array))

   posts = db.crops
   for item in final_tags_array:
   	  try:
   	    result = posts.find_one({'crop_type':item})
   	    your_keys = ["crop_type","market_value","fertilizers"]
   	    dict_you_want = { your_key: result[your_key] for your_key in your_keys }
   	    cropDetails.append(json.dumps(dict_you_want))
   	  except:
   	  	print("Item not found")
      

   return str({'data':final_tags_array,'info':cropDetails})

if __name__ == '__main__':
   app.run(debug = True)