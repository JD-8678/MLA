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

@app.route('/vclaims', methods=['POST','GET'])
def vclaims():
    input = flask.request.args['input']
    mode = flask.request.args['mode']
    # file = 'output\\' + hashlib.md5(url.encode()).hexdigest() + '.json'
    if mode == 'url':
        print('url')
        res = bin.run_url.run(input)
    
    if mode == 'path':
        print('path')

    if mode == 'string':
        print('string')

    # file = 'output\\' + hashlib.md5(url.encode()).hexdigest() + '.json'
    return flask.render_template('/vclaims.html', result=res) 
     
    #except:
    #    return flask.redirect(flask.url_for('title'))

    #if flask.request.method == 'POST':
    #    task_content = flask.request.form['content']
    #    print("post" + str(task_content))
    #
    #    if task_content == None:
    #        return flask.redirect(flask.url_for('title'))
    #
    #    res = bin.run_url.run(task_content)
    #
    #    return flask.render_template('/main.html', result=res)
    #elif flask.request.method == 'GET':
    

    ############# newst
    # if flask.request.method == 'GET': 
    #     if os.path.exists(file):
    #         with open(file, 'r', encoding='utf-8') as myfile:
    #             print("file open")
    #             data = myfile.read()
    #             res = json.loads(data)
    #             myfile.close()  
    #     else:
    #         if flask.request.form.getlist('mode') == "url":
    #             data = bin.run_url.run(url)
    #             res = json.loads(data)
    #             print("test")
    #         else:
    #             data = bin.run_file.run(url)
    #             res = json.loads(data)
    #             print("run_String")
    #     return flask.render_template('/main.html', result=res)


if __name__ == "__main__":
        app.run(debug=True)