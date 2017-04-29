from flask import Flask, send_file, render_template, make_response, send_from_directory
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

def download_images(ids):

	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	for id in ids:
		filename = str(id) + ".jpg"
		url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"  + id + ".jpg"
	
		print(url)
		r = requests.get(url, headers = headers, stream = True)
		print("Request successful")

		# imgIO = StringIO.StringIO()
		imgIO = io.BytesIO()
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				imgIO.write(chunk)

		imgIO.seek(0)

	print("Files downloaded succesfully")

	return True

	# return send_file(imgIO, 
	# 	attachment_filename=filename, 
	# 	as_attachment=True)

@app.route('/app2')
def download_image_2(id=29021):
	image_folder = 'thisisit'
	os.makedirs(image_folder)
	filename = str(id) + ".jpg"
	url2 = "https://wallpaperss.wallhaven.cc/wallpapers/full/wallhaven-"  + str(id) + ".jpg"
	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-29021.jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
	response = requests.get(url, headers = headers, stream = True)
	# save in image/id.jpg
	with open(os.path.join(image_folder,filename), 'wb') as out_file:
		shutil.copyfileobj(response.raw, out_file)

	# zipf = zipfile.ZipFile('images.zip', 'w', zipfile.ZIP_DEFLATED)
	# for root, dirs, files in os.walk(image_folder):
	# 	for file in files:
	# 		zipf.write(os.path.join(root, file))
	# zipf.close()

	# zip out the image folder
	zipf = zipfile.ZipFile('images.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(image_folder):
	    for file in files:
	        zipf.write(os.path.join(root, file))
	zipf.close()

	return send_file('images.zip')

@app.route('/file-download/')
def get_image_ids():
	wallhaven_random_url = "https://alpha.wallhaven.cc/random"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	wallhaven_req = requests.get(wallhaven_random_url, headers=headers, verify=False)
	content = wallhaven_req.text
	soup = BeautifulSoup(content)
	ids = []

	table = soup.find('section', attrs = {'class':'thumb-listing-page'})
	uList = table.find('ul')

	for item in uList.findAll('li'):
	    image_id = item.figure['data-wallpaper-id']
	    ids.append[str(image_id)]

    return(download_image(ids))
	

if __name__ == '__main__':
	app.run(debug=True)
