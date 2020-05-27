from flask import render_template, request
import sqlite3


class Cat:
    def __init__(self, app):
        @app.route('/cat_o_log')
        def main_cat_page():
            # main cat page where you can browse existing cats
            html = """
            <head>
                <title>кот</title>
            </head>
            <body>
                <form action="/cat_o_log/add_cat", method="GET">
                    <button><h4><strong>Добавте вашего кота!</strong></h4></button>
                </form> 

                <form action="/cat_o_log/browse", method="GET">
                    <button><h4><strong>Посмотри на других котов и кошек!</strong></h4></button>
                </form> 
                <form action="/cat_o_log/reset", method="GET">
                    <button><h4><strong>Удали все коты!</strong></h4></button>
                </form>
            </body>
            """

            return html

        @app.route('/cat_o_log/add_cat')
        def add_cat():
            return render_template('add_a_cat.html')

        @app.route('/cat_o_log/get_cat')
        def get_cat():
            connection = sqlite3.connect('services/catopedia.sqlite')
            cursor = connection.cursor()
            listing = (request.args.get('name', None), request.args.get('link', None), request.args.get('description', None))

            cursor.execute("INSERT INTO cats (owner, cat_url, description) VALUES (?, ?, ?)", listing)
            cursor.execute("")

            for cat in cursor.execute("SELECT owner, cat_url, description FROM cats"):
                print(cat)

            connection.commit()
            return render_template('return_to_main_page.html')

        @app.route('/cat_o_log/browse')
        def browse():
            html = """
            <form action="/", method="GET">
                <button><h4><strong>Вернись на главную страницу!</strong></h4></button>
            </form> 
            """
            connection = sqlite3.connect('services/catopedia.sqlite')
            cursor = connection.cursor()

            connection.commit()
            for cat in cursor.execute("SELECT owner, cat_url, description FROM cats"):
                print(cat)

                html += f"<img src='{cat[1]}' style='width:600px;height:500px;' />"
                html += f"<h2>Влоделиц этого питомца: {cat[0]}</h2>"
                html += f"<strong><h2>Описание: </h2></strong>"
                html += f"<p>{cat[2]}</p>"

            return html

        @app.route('/cat_o_log/reset')
        def reset():
            connection = sqlite3.connect('services/catopedia.sqlite')
            cursor = connection.cursor()

            password = input('Enter Password: ')
            if password == 'testing':
                cursor.execute("DELETE FROM cats")
                connection.commit()
                return "<h2>Удолены...</h2>"
            else:
                return "<h2>Не тот пароль =(</h2>"
