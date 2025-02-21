import sys
from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS 
import os


sys.dont_write_bytecode = True

from modules.analytic_execirse.push_up import getExerciseAll

app = Flask(__name__, template_folder='templates')

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    # ตรวจสอบว่าไฟล์ถูกส่งมาหรือไม่
    if 'video' not in request.files:
        return jsonify({'error': 'No video file part'}), 400

    file = request.files['video']
    
    # ตรวจสอบชื่อไฟล์
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # บันทึกไฟล์ที่อัปโหลดลงในโฟลเดอร์
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    return jsonify({'message': 'Video uploaded successfully', 'filename': filename})
@app.route('/reqExerciseAll')
def reqExerciseAll():
    timeStart = 10
    exerciseType = "push_up"
    return Response(getExerciseAll(timeStart, exerciseType), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)