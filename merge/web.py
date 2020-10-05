import flask,csv,json
import os, hashlib
import bin
from bin import lib

app = flask.Flask(__name__)
app.static_folder = 'static'

@app.route("/", methods=['GET', 'POST'])
def index():
    return flask.redirect(flask.url_for("home"))

@app.route('/home', methods=['POST','GET'])
def home():
    if flask.request.method == 'POST':
        task_input = flask.request.form['input']
        task_mode = flask.request.form['mode']
        return flask.redirect(flask.url_for('vclaims', input=task_input, mode=task_mode))
    else:
        return flask.render_template('/home.html')

@app.route("/howto", methods=['GET', 'POST'])
def howto():
  return flask.render_template("howto.html")

@app.route('/vclaims', methods=['GET'])
def vclaims():
    if flask.request.method == 'GET': 
        print("test")
        res = {}
        try:
            input = flask.request.args['input']
            mode = flask.request.args['mode']
        except:
            return flask.redirect(flask.url_for("home"))

        # file = 'output\\' + hashlib.md5(url.encode()).hexdigest() + '.json'
        #if mode == 'url':
        #    print('url')
        #    res = bin.run_url.run(input)
        
        #if mode == 'path':
        #    print('path')

        #if mode == 'string':
        #    print('string')

        json_file = 'output\\' + hashlib.md5(input.encode()).hexdigest() + '.json'
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_file)
        try:
            if os.path.exists(file):
                with open(file, 'r', encoding='utf-8') as myfile:
                    #print("file open")
                    data = myfile.read()
                    res = json.loads(data)
                    myfile.close()  
            else:
                if mode == "url":
                    data = bin.run_url.run(input)
                    res = json.loads(data)
                    #print("run_url")
                else:
                    data = bin.run_file.run(input)
                    res = json.loads(data)
                    #print("run_String")
            
            return flask.render_template('/vclaims.html', result=res) 
        except:
            return flask.redirect(flask.url_for("howto"))

if __name__ == "__main__":
        app.run(debug=True)