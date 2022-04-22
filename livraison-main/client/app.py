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

@app.route('/paiement/<idLivraison>',methods=['GET','POST'])
def paiement(idLivraison):
    if request.method == 'POST':
        json_paiement = {
            "date": request.form.get('dateExpiration')
        }
        response = jsonify(json_paiement)
        r = response.json
        res = requests.post(url=lien+"api/payer/"+idLivraison,json=r)
        
        #res1=str(res.text.split(":")[2].split("}")[0])
        #print(res1)
        return render_template('paiement.html')

    return render_template('paiement.html')


@app.route('/listeLivraison/client')
def listeLivraisonClient():
    mes_livraisons = urllib.request.urlopen(lien+"api/validerLivraison/client").read()
    mes_livraisons = json.loads(mes_livraisons.decode('utf-8'))

    ls = mes_livraisons["livraisons"]

    return render_template("listeLivraisonClient.html",ls=ls)

@app.route('/listeLivraison/livreur')
def listeLivraisonLivreur():
    mes_livraisons = urllib.request.urlopen(lien+"api/validerLivraison/livreur").read()
    mes_livraisons = json.loads(mes_livraisons.decode('utf-8'))

    ls = mes_livraisons["livraisons"]

    return render_template("listeLivraisonLivreur.html",ls=ls)


@app.route('/validerLivraison/client/<idLivraison>',methods=['GET','POST'])
def validerLivraisonClient(idLivraison):
    m = urllib.request.urlopen(lien+"api/validerLivraison/client/"+str(idLivraison)).read()
    m = json.loads(m.decode('utf-8'))

    mess = m['pa']

    return render_template('paiement.html')

@app.route('/validerLivraison/livreur/<idLivraison>',methods=['GET','POST'])
def validerLivraisonLivraison(idLivraison):
    m = urllib.request.urlopen(lien+"api/validerLivraison/livreur/"+str(idLivraison)).read()
    m = json.loads(m.decode('utf-8'))

    mess = m['pa']

    return render_template('paiement.html')


if __name__ == '__main__':
    app.run(host='localhost',port=5007)
