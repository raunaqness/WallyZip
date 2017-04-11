from flask import Flask, send_file
from bs4 import BeautifulSoup
import requests
import os
from PIL import Image
import tempfile

app = Flask(__name__)


def index():
	return (test_image)

@app.route('/', methods=['GET'])
def test_image2():
	buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
	img_url = "http://i.imgur.com/HvPyM85.jpg"

	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-29021.jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	out_dir = 'D:\\'
	r = requests.get(url, headers = headers, stream=True, verify=False)
	if r.status_code == 200:
	    downloaded = 0
	    filesize = int(r.headers['content-length'])
	    for chunk in r.iter_content():
	        downloaded += len(chunk)
	        buffer.write(chunk)
	#         print(downloaded/filesize)
	    buffer.seek(0)
	    print("Open")
	    i = Image.open(io.BytesIO(buffer.read()))
	    i.save(os.path.join(out_dir, 'chal_gya_kya.jpg'), quality=85)
	buffer.close()
	return send_file(i)






def test_image():
	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-29021.jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}

	url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-29021.jpg"
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	path = 'D:\\image3.jpg'
	i = requests.get(url, headers=headers)
	if i.status_code == requests.codes.ok:
	    with iopen(path, 'wb') as file:
	        file.write(i.content)
	else:
	    print("failed")
	return send_file(f, attachment_filename='image.jpg')

def get_image_ids():
	wallhaven_random_url = "https://alpha.wallhaven.cc/random"
	wallhaven_req = urlRequest.Request(wallhaven_random_url, headers = headers)
	content = request.urlopen(wallhaven_req).read()
	soup = BeautifulSoup(content)

	table = soup.find('section', attrs = {'class':'thumb-listing-page'})
	uList = table.find('ul')

	for item in uList.findAll('li'):
	    image_id = item.figure['data-wallpaper-id']
	    download_image(image_id)


def download_image(id):
    url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-" + str(id) + ".jpg"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    
    try:
        req = urlRequest.Request(url, headers = headers)
        path = 'D:\\' + str(id) + '.jpg'
        print("Downloading " + url)
        f = open(path, 'wb')
        f.write(request.urlopen(req).read())
    except urllib.error.HTTPError:
        print ("Page not found!")

if __name__ == '__main__':
	app.run(debug=True)