from flask import Flask, render_template, request
import random
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/page1')
def page1():
    # ....
    html = f"<h1>{random.randint(1,100)}</h1>"
    html += "<img width='200px' src='/static/pig.jpg' /> "
    return html

@app.route('/save')
def save_fake():
    card_number = request.args.get('card_number', None)
    if card_number:
        print(card_number)
    return "Скоро вам придут деньги!"

@app.route('/fake')
def fake():
    return render_template('fake.html')

@app.route('/weather')
def weather():

    temp = random.randint(-20, 40)
    wind_speed = random.randint(0, 20)

    return render_template('pogoda.html', temperature=temp, wind=wind_speed)


app.run(host='0.0.0.0')