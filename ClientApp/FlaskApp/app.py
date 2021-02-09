from flask import Flask, request, url_for,render_template
from werkzeug.utils import secure_filename
import os

from v2.bindLogo import bindCompanyLogo as Labelgen
from v2.genTemplate import generateBaseTemplate as Basetemp
from v2.plotter import plotDatapoints as plt
import v2.AudioToID as AudioID
import v2.IDToHash as Hash
import v2.hashReducer as hr

UPLOAD_FOLDER = './ClientApp/FlaskApp/static/uploads'
ALLOWED_EXTENSIONS = {'wav', 'png'}

app = Flask(__name__)
app.secret_key="12345678"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        if 'FS_audio' not in request.files:
            return render_template('error.html',pos=1)
        if 'FS_image' not in request.files:
            return render_template('error.html',pos=2)
            
        audio = request.files['FS_audio']
        if audio.filename == '':
            return render_template('error.html',pos=3)
            
        if audio and allowed_file(audio.filename) :
            filename = secure_filename(audio.filename)
            audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc1=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logo = request.files['FS_image']
            
        if logo.filename == '':
            return render_template('index.html')
            
        if logo and allowed_file(logo.filename) :
            filename = secure_filename(logo.filename)
            logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            loc2=os.path.join(app.config['UPLOAD_FOLDER'], filename)

        aid =  AudioID.generateAudioID(loc1)
        print("AudioID : " + str(aid))
        sign = Hash.generateHash(aid)
        print("Audio Signatrue : " + str(sign))
        v2Sign = hr.hashReducer(sign, 21)
        print("v2 AudioLabel Signature : " + v2Sign)
        locsave=f"./static/output/{v2Sign}.png"
        print(f'Line 61 {locsave}')
        Labelgen(loc2, 120,locsave)
        print(f'Line 63 {locsave}')
        plt(locsave, locsave, v2Sign)
        print(f'Line 65 {locsave}')
        print(loc1,loc2)
    return render_template('result.html',aid=aid,sign=v2Sign,locsave=locsave)

if __name__ == "__main__":
    app.run(debug=True)
