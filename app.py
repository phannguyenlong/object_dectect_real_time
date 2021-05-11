from flask import Flask, render_template, Response
from flask_mail import Mail, Message
from camera import Camera

app = Flask(__name__)
mail= Mail(app)

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
        frame = camera.get_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/send_mail')
def send_mail() :
    msg = Message('Warning', sender = 'longtestmailserver@gmail.com', recipients = ['phannguyenlong0812@gmail.com'])
    msg.body = "There is some imposter access your store without mask"
    mail.send(msg)
    return "Sent"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')