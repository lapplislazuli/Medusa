import requests
import json
import time

import MedusaMongo as MMongo
import ImageGenerator as MImg
# Variables required through the process

url = 'https://phinau.de/trasi'
access_key = 'ehiefoveingereim3ooD2vo8reeb9ooz'
credentials = {'key': access_key}

# Request functionality
def send_img_bytearray(nipples):
    file_to_upload = {'image': nipples}
    post_request = requests.post(url, files=file_to_upload, data=credentials)
    return post_request

def response_scores_toJSON(post_request):
    if post_request.text:
        return json.loads(post_request.text)

# Full Logic

def full_loop():
    img_bytes = MImg.img_to_bytearray(MImg.create_img_from_bytearray(MImg.create_bytearray()))
    response = send_img_bytearray(img_bytes)
    if(response.status_code==200):
        MMongo.save_results_to_Mongo(response_scores_toJSON(response),img_bytes)
    else:
        print('Error - HTTPStatusCode', response.status_code)

def execute_timed_full_loops(MaxLoops,Intervall):
    print("Starting Scorer Loop")
    i=0
    while(i < MaxLoops):
        full_loop()
        time.sleep(Intervall)
        i+=1
        if(i%100 == 0):
            print("loop #"+str(i) + " done")
    print("Done")
