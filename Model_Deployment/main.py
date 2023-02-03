from flask import Flask, render_template, redirect, request
import webbrowser
from gtts import gTTS
import shutil
from datetime import datetime

from googletrans import *
translator = Translator()
import Caption_it

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# __name__ == __main__
app = Flask(__name__)


@app.route('/')
def hello():
	return render_template("index_new.html")

@app.route('/', methods= ['POST'])
def marks():
    if request.method == 'POST':
        f = request.files['userfile']
        l = request.form.get('lang')
        path = "./static/{}".format(f.filename)# ./static/images.jpg
        f.save(path)
        
        caption = Caption_it.caption_this_image(path)
        caption = translator.translate(caption, dest = l).text
        
        time=datetime.now().strftime("_%H_%M_%S")
        name="test"+time+".mp3"
        #name=`test${time}.mp3
        gTTS(caption,lang=l).save(name)
        shutil.move(name, "./static/"+name)
        audio="./static/"+name
        result_dic = {
        'image' : path,
		'caption' : caption,
        'audio' : audio
		}
        
    return render_template("index_new.html", your_result =result_dic)

if __name__ == '__main__':
	# app.debug = True
	# due to versions of keras we need to pass another paramter threaded = Flase to this run function
    webbrowser.open("http://127.0.0.1:5000/", new=2)
    app.run(debug = False, threaded = False)
