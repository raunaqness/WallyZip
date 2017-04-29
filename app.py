from flask import Flask, send_file, render_template, make_response, send_from_directory, redirect, url_for
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
import tempfile
import io
import shutil
import zipfile

app = Flask(__name__)

@app.route('/')
def home():
	return render_template ('index.html')


def get_image_ids():
	wallhaven_random_url = "https://alpha.wallhaven.cc/random"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	wallhaven_req = requests.get(wallhaven_random_url, headers=headers, verify=False)
	content = wallhaven_req.text
	soup = BeautifulSoup(content)
	image_ids = []
	image_id = ""

	table = soup.find('section', attrs = {'class':'thumb-listing-page'})
	uList = table.find('ul')

	for item in uList.findAll('li'):
	    image_id = str(item.figure['data-wallpaper-id'])
	    image_ids.append(image_id)

	# return(download_images(image_ids))
	return (image_ids)
	
@app.route('/file-download/')
def download_images():

	ids = get_image_ids()

	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	image_folder = 'Images'

	if(os.path.isdir(image_folder)):
		shutil.rmtree(image_folder, ignore_errors=True)

	os.makedirs(image_folder)

	for id in ids:
		filename = str(id) + ".jpg"
		url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"  + id + ".jpg"
	
		print(url)
		response = requests.get(url, headers = headers, stream = True)
		print("Request successful")

		with open(os.path.join(image_folder,filename), 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)

	print("Files downloaded succesfully")

	return redirect(url_for('create_zip'))

@app.route('/zip')
def create_zip():
	image_folder = 'Images'
	zipf = zipfile.ZipFile('images.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(image_folder):
	    for file in files:
	        zipf.write(os.path.join(root, file))
	zipf.close()

	return send_file('images.zip', attachment_filename="GG.zip", as_attachment=True)
	

if __name__ == '__main__':
	app.run(debug=True)
