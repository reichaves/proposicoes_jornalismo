import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import requests
import pandas as pd
import dash_core_components as dcc
import plotly.express as px
import numpy as np
from dash.dependencies import Input,Output
import dash_table
import io
import os
import datetime

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)



PLOTLY_LOGO = "https://www.portaldosjornalistas.com.br/wp-content/uploads/2019/09/Abraji.png"


navbar = dbc.Navbar(
        [
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px"), ),
                        
                        dbc.Col(
             dbc.NavbarBrand("App Title", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            ),
             ),

                    ],
                    align="center",
                    className="g-10",
                ),
            
            dbc.Row(
            [
        dbc.Col(
        dbc.Button(id = 'button', children = "Click Me!", color = "primary"), 
            )        
    ],
            # add a top margin to make things look nice when the navbar
            # isn't expanded (mt-3) remove the margin on medium or
            # larger screens (mt-md-0) when the navbar is expanded.
            # keep button and search box on same row (flex-nowrap).
            # align everything on the right with left margin (ms-auto).
     className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
)
            
         ],
)


app.layout = html.Div(id = 'parent', children = [navbar])

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



if __name__ == "__main__":
    app.run_server()


