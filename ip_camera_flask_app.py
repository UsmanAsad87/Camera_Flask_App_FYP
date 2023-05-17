from flask import Flask, render_template, Response, request
import requests
import cv2
import datetime, time
import os, sys
import numpy as np
import base64
from threading import Thread
import argparse


global rec_frame,switch,  rec, show,counter
switch=1
rec=0
show=0
counter=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass


#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

ipCamUrl='http://192.168.0.105:8080/video'
# camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture(ipCamUrl)
# camera = cv2.VideoCapture('http://192.168.0.105:4747/video')

def record():
    global rec_frame,show,counter
    while(rec):
        time.sleep(0.2)
        #print(rec_frame.shape)

        if( show==0):
            try:
                tic=time.time()
                print(type(rec_frame))
                res, frame = cv2.imencode('.jpg', rec_frame)   
                b64 = base64.b64encode(frame) 
                img = "data:image/jpeg;base64," + b64.decode('utf-8')
                api_url = "http://192.168.0.106:5000/findface"
                # api_url = "http://172.30.34.64:5000/findface"
                print(api_url)
                
                data= {
                     "model_name": "ArcFace",
                     "location":"lab ICV",
                     "img":img
                }
                response = requests.post(api_url, json=data)
                print(response.json())
                print("Count: "+str(counter))
                counter=counter+1
                toc=time.time()
                print("Time taken: "+str(toc-tic))

            except Exception as e:
                print(e)
                show=1
                


        #print(len(b64.decode('utf-8')))
        # if(show==0):
        #     with open('readme.txt', 'w') as f:
        #         f.write(b64.decode('utf-8'))
        #     show=1

        #out.write(rec_frame)


 

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:  
            if(rec):
                rec_frame=frame
                frame= cv2.putText(cv2.flip(frame,1),"Tracking...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
    
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST': 
        if  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
                
            else:
                camera = cv2.VideoCapture(ipCamUrl)
                switch=1
        elif  request.form.get('rec') == 'Start/Stop Service':
            global rec, out
            rec= not rec
            if(rec):
                print("rec")
                thread = Thread(target = record)
                thread.start()
            elif(rec==False):
                #out.release()
                pass
                          
                 
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
		'-p', '--port',
		type=int,
		default=5000,
		help='Port of serving api')
    args = parser.parse_args()
	#app.run(host='0.0.0.0', port=80,debug=False)
    #app.run(host='0.0.0.0', port=args.port,debug=True)
    app.run(debug=True)
    # app.run()
camera.release()
cv2.destroyAllWindows()     