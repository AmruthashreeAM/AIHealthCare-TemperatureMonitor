from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api
import easyocr
import os
import cv2, re
import csv
from datetime import datetime
import pandas as pd
import json
import cv2
import time 

#import pymongo
#from pymongo import MongoClient
#CONNECTION_STRING = "mongodb+srv://sxm4311:soumya123@cluster0.s89sh.mongodb.net/test?authSource=admin&replicaSet=atlas-pxhlmq-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true"
#client = MongoClient(CONNECTION_STRING)

#import frames

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/generateRecords')
def capture():
        captureImages()
        for filename in os.listdir('./raidimages'):
            img=cv2.imread(os.path.join('./raidimages',filename))
            reader=easyocr.Reader(['en'])
            results=reader.readtext(img)
            text=''
            for result in results:
                try:
                    if 'S:' in result[1]:
                        S=float((re.findall("\d+\.+\d", str(result[1])))[0])
                    elif 'H:' in result[1]:
                        H=float((re.findall("\d+\.+\d", str(result[1])))[0])
                except Exception as e:
                    S=0
                    H=0
            now=datetime.now()
            current_time=now.strftime(("%Y/%m/%d %H:%M:%S"))

            name= "amrutha"

            data=[name,"39", "39",current_time]
            # with open('/Users/kranthi/Downloads/AIBasedHealthTracker/AIHealthCare-server/routes/tempData.csv', mode='a', newline='') as csv_file:
            #     csv_file.columns = ['patientName' 'temperatureNow' 'temperatureSoFar' 'recordedDateTime'] 
            #     writer=csv.writer(csv_file)
            #     writer.writerow(data)
            # csv_file.close()
        
            response = json.dumps({'temperatureNow': H, 'temperatureSoFar':S, 'recordedDateTime' : datetime.now().strftime("%Y/%m/%d %H:%M:%S")})
            return  response

def captureImages():
    capture = cv2.VideoCapture(1)
    frameNr = 0

    dur=6
    start=time.time()
    while (True) and time.time()<start+dur:
    
        success, frame = capture.read()
        #start = time.time()
        if success:
            time.sleep(5)
            cv2.imwrite(f'./raidimages/frame_{frameNr}.jpg', frame)
    
        else:
            break
    
        frameNr = frameNr+1
        cv2.waitKey(1)
    
    capture.release()

if __name__ == '__main__':
     app.run(host="localhost", port=5000)


