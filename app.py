from flask import Flask, render_template, Response, redirect, url_for
from flask_mail import Mail, Message
import requests
from camera import Camera
from playsound import playsound
from HOG.svm import *
from HOG import *
import cv2
app = Flask(__name__)
mail = Mail(app)
frame = None # frame use for sending mail (set to global in function)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'longtestmailserver@gmail.com'
app.config['MAIL_PASSWORD'] = "@longlong123"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        global frame
        frame1 = camera.get_rawFrame()
        if(type(Result(frame1))!=int):
            frame = camera.convert_frame(frame1)
            print("Not mask")
            break
        else:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(camera.convert_frame(frame1)) + b'\r\n')
    requests.get("http://127.0.0.1:5000/send_mail");

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/send_mail')
def send_mail() :
    msg = Message('Warning', sender = 'longtestmailserver@gmail.com', recipients = ['lmht772000@gmail.com'])
    msg.body = "There is some imposter access your store without mask"
    msg.attach("image.jpg", "image/jpeg", bytearray(frame))
    mail.send(msg)
    playsound('warning.wav')
    return "Sent"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')