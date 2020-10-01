import flask,csv,json
import os
import bin

app = flask.Flask(__name__)
app.static_folder = 'static'

@app.route('/', methods=['POST','GET'])
def title():
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        print(task_content)

        return flask.redirect(flask.url_for('index',url=task_content))
    else:
        return flask.render_template('/title_page.html')


@app.route('/search/', methods=['POST','GET'])
def index():
    url = flask.request.args['url']
    #try:
    res = bin.run_url.run(url)
    return flask.render_template('/main.html', result=res) 
    #except:
    #    return flask.redirect(flask.url_for('title'))

    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        print(task_content)

        if task_content == None:
            return flask.redirect(flask.url_for('title'))

        res = bin.run_url.run(task_content)

        return flask.render_template('/main.html', result=res)

if __name__ == "__main__":
        app.run(debug=True)