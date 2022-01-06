import datetime
import io
import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])

def telegram():
	# Processa mensagem
	update = request.json
	chat_id = update["message"]["chat"]["id"]
	text = update["message"]["text"].lower()
	
	if text in ['oi', 'olá', 'ola']:
		answer = "Oi, como vai?!"
  	elif text in ['bom dia', 'boa tarde', 'boa noite']:
		answer = text
	elif "jornalismo" in text:
		answer = "Em breve..."
	else:
		answer = "Não entendi!!!"
	
  	# Responde mensagem
	token = os.environ["TELEGRAM_TOKEN"]
	message = {"chat_id": chat_id, "text": answer}
	url = f"https://api.telegram.org/bot{token}/sendMessage"
	response = requests.post(url, data=message)
	
	if response.json()["ok"] == False:
		raise RuntimeError("Erro ao responder API do Telegram")
	
	return "ok"
