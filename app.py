import requests
import pandas as pd
import io
import os
import datetime
from flask import Flask, render_template, request
import os
import base64
import json
import gspread 
import datetime


spreadsheet_id = os.environ["GOOGLE_SHEET_ID2"]
conteudo_codificado = os.environ["GOOGLE_SHEET_CREDENTIALS1"]

conteudo = base64.b64decode(conteudo_codificado)
credentials = json.loads(conteudo)

service_account = gspread.service_account_from_dict(credentials) # autenticação
spreadsheet = service_account.open_by_key(spreadsheet_id) # "abrir" o arquivo
worksheet = spreadsheet.worksheet("Página1") # aba

app = Flask(__name__)



@app.route("/telegram", methods=["POST"])

def telegram():
	# Processa mensagem
	datahora = str(datetime.datetime.now())
	update = request.json
	chat_id = update["message"]["chat"]["id"]
	text = update["message"]["text"].lower()
	if "username" in update["message"]["from"]:
		username = update["message"]["from"]["username"]
	else:
		username = ""
	first_name = update["message"]["from"]["first_name"]
	last_name = update["message"]["from"]["last_name"]
	
	#Guarda na planilha a mensagem recebida
	worksheet.append_row([datahora, chat_id, "robot", username, first_name, last_name, text])
	
	if text in ['oi', 'olá', 'ola']:
		answer = "Oi, como vai?!"
	elif text in ['bom dia', 'boa tarde', 'boa noite']:
		answer = text
	elif "jornalismo" in text:
		answer = "No momento eu monitoro na Abraji em jornalismo apenas o projeto que coleta proposições legislativas de interesse do jornalismo brasileiro, veja aqui: https://jornalismonocongresso.herokuapp.com - Em breve eu vou mnonitorar mais projetos e trazer informações aqui :)"
	elif "robô" or "robot" in text:
		answer = "Sim, pois é sou um robot :) Mas com uma limitação de respostas. Se você tem mais dúvidas sobre o trabalho da Abraji escreva para: abraji@abraji.org.br"
	else:
		answer = "Desculpe, não entendi. Sou um robô com uma limitação de respostas. Se você tem mais dúvidas sobre o trabalho da Abraji escreva para: abraji@abraji.org.br"
	
  	# Responde mensagem
	token = os.environ["TELEGRAM_TOKEN"]
	message = {"chat_id": chat_id, "text": answer}
	url = f"https://api.telegram.org/bot{token}/sendMessage"
	response = requests.post(url, data=message)
	
	if response.json()["ok"] == False:
		raise RuntimeError("Erro ao responder API do Telegram")
	
	return "ok"

