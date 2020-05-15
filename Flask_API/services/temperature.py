import json
import random


class TemperatureApp:
    def __init__(self, app):

        @app.route('/temp')
        def generate_temp():
            temperature = random.randint(-30, 40)
            country = random.choice(json.load(open('services/countries.txt', 'r')))

            html = f'<h1>Сейчас в {country} {temperature} градусов.</h1>'
            html += '<h2>Вот вам картинка описывая критичную ситуацы:</h2>'

            if temperature <= 10:
                html += '<img src = "/static/snowy.jpeg" />'
                html += '<h2>Сежный опакалипсис!</h2>'

            if 10 < temperature <= 24:
                html += '<img src = "/static/normalicy.jpg" />'
                html += '<h2>Как обычно... Без проблем... Не бомби.</h2>'

            if temperature > 24:
                html += '<img src = "/static/new_hot.jpeg" />'
                html += '<h1>Возми пивка, выйди на улицу и станцуй под хардбасс потому что сегодня жарко.</h2>'

            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """

            return html
