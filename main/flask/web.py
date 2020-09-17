import flask,csv,json
import os
import run,argparse

app = flask.Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    if flask.request.method == 'POST':
        task_content = flask.request.form['content']
        #reader = csv.reader(open('result.csv'),delimiter=',')
        #exec("python ./../run.py -i 'TestString'")
        print(task_content)
        #result = os.system('python ./../run.py -m ' + flask.request.form['mode'] + ' -i ' + task_content )
        args = parse_args(flask.request.form['mode'],task_content)
        #result,maintext = run.main(args)
        #print(result.values)
        #reader=result.values
        reader=[["elem_0","elem_1","elem_2","elem_3","elem_4"]]
        maintext = "This is the maintext"
        return flask.render_template('main.html', claims=reader, text=maintext)
    else:
        return flask.render_template('main.html', claims=[[]])

def parse_args(mode,input):
    parser = argparse.ArgumentParser()
    parser.add_argument("--predict-file", "-p", default="result.csv",
                        help="File in TREC Run format containing the model predictions")
    parser.add_argument("--keys", "-k",nargs='+', default=['vclaim', 'title', 'named_entities_claim', 'named_entities_article','keywords'],
                        help="Keys to search in the document")
    parser.add_argument("--size", "-s", default=10000,
                        help="Maximum results extracted for a query")
    parser.add_argument("--output_size", "-x", default=10000,
                        help="Maximum results extracted for news")
    parser.add_argument("--conn", "-c", default="127.0.0.1:9200",
                        help="HTTP/S URI to a instance of ElasticSearch")
    parser.add_argument("--mode", "-m", default="url", choices=["url","string"], type=str.lower,
                        help="choice between url or string mode")
    parser.add_argument("--input", "-i", nargs='+', required=True,
                        help="input should be a String or url")
    return parser.parse_args(['--mode',mode,'--input',input])

if __name__ == "__main__":
        app.run(debug=True)