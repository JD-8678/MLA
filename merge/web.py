import flask,csv,json
import os,hashlib
import bin

app = flask.Flask(__name__)
app.static_folder = 'static'

@app.route('/', methods=['POST','GET'])
def title():
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        print("title Post" + str(task_content))

        return flask.redirect(flask.url_for('index',url=task_content))
    else:
        return flask.render_template('/title_page.html')

@app.route('/search/', methods=['POST','GET'])
def index():
    url = flask.request.args['url']
    file = 'output\\' + hashlib.md5(url.encode()).hexdigest() + '.json'

    res = None
     
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
    if flask.request.method == 'GET': 
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as myfile:
                print("file open")
                data = myfile.read()
                res = json.loads(data)
                myfile.close()  
        else:
            if flask.request.form.getlist('mode') == "url":
                data = bin.run_url.run(url)
                res = json.loads(data)
                print("test")
            else:
                data = bin.run_file.run(url)
                res = json.loads(data)
                print("run_String")
        return flask.render_template('/main.html', result=res)


if __name__ == "__main__":
        app.run(debug=True)