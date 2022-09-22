import urllib.request
import json
import os
import ssl
from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/')
@app.route('/homepage', methods=["GET","POST"])
def homepage():

    if request.method == 'POST':
        data = request.form['content']

        body = str.encode(json.dumps(data))
        try:

            req = urllib.request.Request(url, body, headers)
            response = urllib.request.urlopen(req)
            result = response.read()

            result = re.sub('\"','',str(result, 'UTF-8'))
            words = result.split(" ")
            words[0], words[-1] = words[0].strip("\\"), words[-1].strip("\\")

            summary = ' '.join(words)

            data_from_backend = [{"title":'Actual text',"text":body.decode()},{"title":'Summary text',"text":summary}]
            return render_template('summarised.html', message=data_from_backend)

        except:

            print("Error occured")    
            return render_template('homepage.html')
    else:

        return render_template('homepage.html')

if __name__ == "__main__":

    def allowSelfSignedHttps(allowed):

        if allowed and not os.environ.get("PYTHONHTTPSVERIFY",'') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True)

    url = 'http://52.191.39.188.80/api/v1/service/text-summarisation-5/score'
    api_key = 'eHbpe93rUKCLKAkuvR9HnxRXLMKVTCA3'

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer'+api_key)}

    app.run(debug=True)