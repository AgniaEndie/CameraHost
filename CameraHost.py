import random

import cv2
import requests
from flask import Flask, Response

app = Flask(__name__)
video = cv2.VideoCapture(0)


def generate_frames():
    while True:
        success, frame = video.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_capture')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    server_addr = "localhost:30081"
    app.run(host='0.0.0.0', port=8080, debug=True)
    IP = requests.get('https://api.ipify.org/').text
    ip_port = f'{IP}:{8080}/video_capture'
    requests.post(server_addr, json={
        "name": f"foxwatch{random.randint(0,100)}",
        "ip": ip_port
    })