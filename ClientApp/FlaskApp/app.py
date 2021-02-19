from flask import Flask, request, url_for,render_template,send_file
from werkzeug.utils import secure_filename
import os

from v2.bindLogo import bindCompanyLogo as Labelgen
from v2.genTemplate import generateBaseTemplate as Basetemp
from v2.plotter import plotDatapoints as plt
import v2.AudioToID as AudioID
import v2.IDToHash as Hash
import v2.hashReducer as hr
from v2.v2ImageToSubSign import imageToSubSignature as decoder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'wav', 'png'}

app = Flask(__name__)
app.secret_key="12345678"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'

db=SQLAlchemy(app)

class Label(db.Model):
    ID=db.Column('ID',db.Integer,primary_key=True, autoincrement=True)
    AID=db.Column('AID',db.Text)
    SubSignature=db.Column('SubSignature',db.Text)
    label_loc=db.Column('label_loc',db.Text)
    audio_loc=db.Column('audio_loc',db.Text)
    def _init_(self,ID,AID,SubSignature,label_loc,audio_loc):
        self.ID=ID
        self.AID=AID
        self.SubSignature=SubSignature
        self.label_loc=label_loc
        self.audio_loc=audio_loc


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
        print(loc1,loc2)
        Labelgen(loc2, 120,locsave)

        plt(locsave, locsave, v2Sign)
        label_temp=Label(AID=aid,SubSignature=v2Sign,label_loc=locsave,audio_loc=loc1)
        print(label_temp)
        db.session.add(label_temp)
        db.session.commit()

        lb=db.session.query(Label).filter_by(AID=aid).first()
        if lb == None:
            return render_template('error.html',pos='not found aid')
        print(loc1,loc2)
    return render_template('result.html',aid=lb.AID,sign=lb.SubSignature,locsave=lb.label_loc)

@app.route('/decode',methods=['POST'])
def decode():
    if request.method== 'POST':
        try:
            if 'check_image' not in request.files:
                return jsonify({"Message":"send an image to decode"})
            img=request.files['check_image']
            if img and allowed_file(img.filename) :
                filename = secure_filename(img.filename)
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                loc_check=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            subsigns=decoder(loc_check)
            for subsign in subsigns:
                lb=db.session.query(Label).filter_by(SubSignature=subsign).first()
                if lb != None:
                    break
            if lb != None:
                return send_file(lb.audio_loc,mimetype="audio/wav",as_attachment=True,attachment_filename="audio.wav")
            else:
                return jsonify({"Message":"Not Found in Database"})
        except:
            return jsonify({"Message":"Oops Something Went Wrong"})

if __name__ == "__main__":
    app.run(debug=True)
