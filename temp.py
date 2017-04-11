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

if __name__ == '__main__':
	app.run(debug=True)