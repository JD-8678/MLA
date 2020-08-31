import flask,csv,json

app = flask.Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if flask.request.method == 'POST':
        #task_content = flask.request.form['content']
        reader = csv.reader(open('result.csv'),delimiter=',')
        return flask.render_template('main.html', claims=reader)
    else:
        return flask.render_template('main.html', claims=[[]])

if __name__ == "__main__":
        app.run(debug=True)