from flask import Flask, flash, redirect, render_template, request, session, send_file
from time import strftime, gmtime
from re import sub

from pytube import YouTube

# Start Flask
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Secret key to enable session
app.secret_key = """Put your secret key here"""



@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        
        link = request.form.get('link')
        session["link"] = link
        if link == '':
            flash("URL not provided!", "info")
            return redirect('/')
        yt = YouTube(link)   
        author = yt.author
        thumbnail = yt.thumbnail_url
        length = yt.length
        title = yt.title

        if int(length) <= 3599:
            time = strftime("%M:%S", gmtime(length))
        else:
            time = strftime("%H:%M:%S", gmtime(length))

        return render_template("converted.html", author=author, thumbnail=thumbnail, time=time, title=title)

    else:
        return render_template("index.html")

@app.route('/converted', methods=['GET', 'POST'])
def converted():

    if request.method == 'POST':
        
        link = session.get("link", None)
        yt = YouTube(link) 
        f_for = request.form.get('file-format')

        if f_for == '48kbps' or f_for == '128kbps':

            ys = yt.streams.filter(only_audio=True).first()
            title = sub("[!@#$"'"'"'/\|?*<>:{&}~%+-=]", "", yt.title)
            return send_file(ys.download(filename=f'{title}.mp3'), as_attachment=True)
            
        else: 

            # Store the stream you'd like to get according to the selected resolution
            ys = yt.streams.filter(file_extension='mp4', res=f_for).first()
            # Download video
            return send_file(ys.download(), as_attachment=True)


    else:

        return render_template("converted.html")

if __name__ == '__main__':
    app.run(debug=True)