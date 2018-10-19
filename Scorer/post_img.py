#Requires Anaconda to be functioning without extra Installs
import requests
from PIL import Image

url = 'https://phinau.de/trasi'
# API-Key
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
filename = 'sample.png'
# Key-Value pair: API-Key
credentials = {'key': access_key}

def load_image(path):
    try:  
        img  = Image.open(path)  
        return img 
    except IOError: 
        print("File seems to be non existant or no image")

def test_connection():
    get_request = requests.get(url)
    print(get_request.status_code)
    print(get_request.text)
#test_connection()

def post_img(path):
    img = open(path, "rb").read()
    JSONImg = {'image': img}
    
    post_request = requests.post(url, files=JSONImg , data=credentials)
    # Get Status Code of the sent GET-Request
    print(post_request.status_code)
    # Print out the Text to the GET-Request
    print(post_request.text)

def show_img(path):
    img = load_image(path)
    img.show()

#show_img("random1.png")

post_img('random1.png')
post_img('random2.png')
post_img('random3.png')
