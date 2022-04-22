from flask import render_template, request, Flask, flash, jsonify, redirect, url_for
import json
import urllib.request
import requests
app = Flask(__name__)

lien="http://127.0.0.1:5007/"


@app.route('/')
def connexion():
    test1 = urllib.request.urlopen(lien).read()
    test1 = json.loads(test1.decode('utf-8'))

    test = test1["test"]

    return render_template('connexion.html',t=test)

@app.route('/inscription')
def inscription():
    return render_template('inscription.html')

@app.route('/livreur')
def livreur():
    return render_template('livreur.html')


@app.route('/client')
def client():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(host='localhost',port=5007)
