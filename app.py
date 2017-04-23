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


@app.route('/file-download/')
def test():
	filename = str(id) + ".jpg"
	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-169777.jpg"
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
	

@app.route('/file-download/')
def download_image(id):
	filename = str(id) + ".jpg"
	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-" + str(id) + ".jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	
	print(url)
	r = requests.get(url, headers = headers, stream = True)
	print("Request successful")

	# imgIO = StringIO.StringIO()
	imgIO = io.BytesIO()
	for chunk in r.iter_content(chunk_size=1024):
		if chunk:
			imgIO.write(chunk)

	imgIO.seek(0)

	return send_file(imgIO, 
		attachment_filename=filename, 
		as_attachment=True)

if __name__ == '__main__':
	app.run(debug=True)