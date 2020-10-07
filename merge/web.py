import flask,csv,json
import numpy as np
import pandas as pd
import os, hashlib
from bin import lib
import bin
import json
from  elastic_search_create import build_index, clear_index

app = flask.Flask(__name__)
app.static_folder = 'static'

@app.route("/", methods=['GET', 'POST'])
def index():
    return flask.redirect(flask.url_for("home"))

@app.route('/home', methods=['POST','GET'])
def home():
    if flask.request.method == 'POST':
        if flask.request.form["submit"] == "submit":
            task_input = flask.request.form['input']
            task_connection = flask.request.form['elastic']
            task_index = flask.request.form['index']
            task_output = flask.request.form['output']
            task_mode = flask.request.form['mode']
            return flask.redirect(flask.url_for('vclaims', input=task_input, mode=task_mode, client=task_connection, index=task_index, output=task_output))
        elif flask.request.form["submit"] == "status":
            task_connection = flask.request.form['elastic']
            task_index = flask.request.form['index']
            return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))
    else:
        return flask.render_template('/home.html')

@app.route("/howto", methods=['GET', 'POST'])
def howto():
  return flask.render_template("howto.html")

@app.route("/status", methods=['GET', 'POST'])
def status():
    if flask.request.method == 'POST':
        try:
            if flask.request.form["dl"] == "download":
                lib.check_model(download=True)
                task_connection = flask.request.form['elastic']
                task_index = flask.request.form['index']
                return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))

            elif flask.request.form["dl"] == "create":
                task_index = flask.request.form['index']
                task_connection = flask.request.form['elastic']
                task_bool = flask.request.form['index_bool']
                if task_bool == "False":
                    client = lib.create_connection(task_connection)
                    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bin' ,'data','vclaims.tsv')
                    index_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bin', 'data','index.json')
                    vclaims = pd.read_csv(path, sep='\t',  index_col=0)
                    keys = ['title',
                            'vclaim',
                            'ratingName',
                            'author',
                            'named_entities_article',
                            'named_entities_claim',
                            'link',
                            'keywords',
                            'date',
                            'vector']
                    build_index(CLIENT=client, VCLAIMS=vclaims, INDEX_FILE=index_file, INDEX_NAME=task_index, KEYS=keys)
                    return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))
                else:
                    return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))
            
            elif flask.request.form["dl"] == "clear":
                task_index = flask.request.form['index']
                task_connection = flask.request.form['elastic']
                task_bool = flask.request.form['index_bool']
                if task_bool == "True":
                    client = lib.create_connection(task_connection)             
                    clear_index(CLIENT=client, INDEX_NAME=task_index)
                    return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))
                else:
                    return flask.redirect(flask.url_for('status', elastic=task_connection, index=task_index))
        except:
            return flask.redirect(flask.url_for("howto"))


    elif flask.request.method == 'GET': 
        res = {}
        elastic = flask.request.args['elastic']
        index = flask.request.args['index']
        data = lib.status(elastic=elastic, index=index)
        data["input_elastic"] = elastic
        data["input_index"] = index
        return flask.render_template("status.html", result=data)
        


@app.route('/vclaims', methods=['GET'])
def vclaims():
    if flask.request.method == 'GET': 
        res = {}
        try:
            input = flask.request.args['input']
            mode = flask.request.args['mode']
            client = flask.request.args['client']
            index = flask.request.args['index']
            output = flask.request.args['output']
        except:
            return flask.redirect(flask.url_for("home"))
        json_file = output + '\\' + hashlib.md5(input.encode()).hexdigest() + '.json'
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), json_file)
        try:
            # if os.path.exists(file):
            #     with open(file, 'r', encoding='utf-8') as myfile:
            #         #print("file open")
            #         data = myfile.read()
            #         res = json.loads(data)
            #         myfile.close()  
            # else:
            if mode == "url":
                data = bin.run_url.run(input=input, client=client, output_path = output_path, index_name=index)
                res = json.loads(data)
                return flask.render_template('/vclaims.html', result=res)
            else:
                if mode == "text" or mode == "file":
                    data = bin.run_text.run(input=input, client=client, output_path = output_path, index_name=index)
                    res = json.loads(data)
                    return flask.render_template('/vclaims.html', result=res) 
        except:
            return flask.redirect(flask.url_for("howto"))

if __name__ == "__main__":
        app.run(debug=True)