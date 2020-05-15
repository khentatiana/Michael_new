from flask import Flask
from Flask_API.services.calculator import *
from Flask_API.services.credit_card import *
from Flask_API.services.temperature import *
from Flask_API.services.cat_o_pedia import *

app = Flask(__name__)


@app.route('/')author
def main():
    return render_template('main.html')


# temperature web service
temp = TemperatureApp(app)

# scamming web service section
scam = CreditCard(app)

# calculator web service section
calculator = Calculator(app)

# cat-o-pedia web service section
cats = Cat(app)

app.run(debug=True)
