from flask import Flask, send_file, render_template
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
import tempfile
import io

app = Flask(__name__)

@app.route('/')
def home():
	return render_template ('index.html')

def download_image(id):
	filename = str(id) + ".jpg"
	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-"  + id + ".jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
	# print(url)
	r = requests.get(url, headers = headers, stream = True)
	# print("Request successful")

	# imgIO = StringIO.StringIO()
	imgIO = io.BytesIO()
	for chunk in r.iter_content(chunk_size=1024):
		if chunk:
			imgIO.write(chunk)

	imgIO.seek(0)

	return send_file(imgIO, 
		attachment_filename=filename, 
		as_attachment=True)

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

	zipf = zipfile.ZipFile('images.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(image_folder):
		for file in files:
			zipf.write(os.path.join(root, file))
	zipf.close()

	zipf2 = zipfile.ZipFile(os.path.abspath('images.zip'), 'r', zipfile.ZIP_DEFLATED)

	# response = send_from_directory (os.path.abspath('images.zip'), 'images.zip', as_attachment=True,
 #                attachment_filename="images.zip",
 #                mimetype='application/zip')

	# return response

	return send_file(zipf2,
		mimetype = 'application/zip',
		as_attachment=True)

	# if response.status_code == 200:
	# 	return response(response.content,
	# 		mimetype = 'application/zip',
	# 		headers={'Content-Description' : 'attachment; filename=zones.zip'})

	# zipf = zipfile.ZipFile('images.zip', 'r', zipfile.ZIP_DEFLATED)
	# return response(zipf, 
	# 	mimetype = 'application/zip',
	# 	headers = {'Content-Description' : 'attachment; filename = zones.zip'})


@app.route('/file-download/')
def index():
	wallhaven_random_url = "https://alpha.wallhaven.cc/random"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	wallhaven_req = requests.get(wallhaven_random_url, headers=headers, verify=False)
	content = wallhaven_req.text
	soup = BeautifulSoup(content)
	ids = ""

	table = soup.find('section', attrs = {'class':'thumb-listing-page'})
	uList = table.find('ul')

	for item in uList.findAll('li'):
	    image_id = item.figure['data-wallpaper-id']
	    ids = ids + " " + str((image_id))
	    return(download_image(image_id))
	

if __name__ == '__main__':
	app.run(debug=True)