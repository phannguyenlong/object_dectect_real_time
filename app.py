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
delay = 0
path = os.path.dirname(os.path.abspath(__file__))

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
        global delay
        frame1 = camera.get_rawFrame()
        frame = camera.convert_frame(frame1)

        if(type(Result(frame1))!=int):
            delay = delay +1
            print("Not mask")
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(
                frame) + b'\r\n')
            if(delay==3):
                frame = camera.convert_frame(frame1)
                break
        elif (Result(frame1) == 1):
            delay=0
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(
                frame) + b'\r\n')
            continue
        else:
            delay = 0
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')
    requests.get("http://127.0.0.1:5000/send_mail");
    playsound(os.path.sep.join([path, "warning.wav"]))

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
    return "Sent"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')