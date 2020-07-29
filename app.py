from flask import render_template
from flask import flash, Flask
from flask import request, redirect, url_for
import requests

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

items = data[-1].get("rates")

app = Flask(__name__)

def calculate_amount_pln(amount, currency, items):
    for i in items:
        if i["currency"] == currency:
            try:
                return round(float(i["bid"]) * float(amount),2)
            except:
                return "Podaj kwotę jako liczbę"

@app.route("/calculator", methods=['GET', 'POST'])
def calculate_currency():
    if request.method == 'POST':
        error = None
        currency = request.form.get('currency_value')
        amount = request.form.get('amount')
        amount_in_pln = calculate_amount_pln(amount,currency, items)
        if isinstance(amount_in_pln, (int, float)):
            return render_template('main_page.html', amount_in_pln=amount_in_pln, items=items)
        else:
            return render_template('main_page.html', items=items, error=amount_in_pln)
        
    elif request.method == 'GET':
        return render_template('main_page.html', items=items)



