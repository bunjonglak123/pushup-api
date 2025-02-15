import sys
from flask import Flask, render_template, Response


sys.dont_write_bytecode = True

from modules.analytic_execirse.push_up import getExerciseAll

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reqExerciseAll')
def reqExerciseAll():
    timeStart = 10
    exerciseType = "push_up"
    return Response(getExerciseAll(timeStart, exerciseType), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)