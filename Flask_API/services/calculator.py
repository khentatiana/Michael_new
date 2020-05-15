# calculator web service section
from flask import render_template, request
import math


class Calculator:
    def __init__(self, app):
        @app.route('/calculator')
        def calculator():
            return render_template('calculator.html')

        @app.route('/calculator/pythag')
        def pythagorean():
            return render_template('pythagorean.html')

        @app.route('/calculator/pythagorean_calculated')
        def calc_pythagorean():
            a = int(request.args.get('a', None))
            b = int(request.args.get('b', None))
            html = ''
            if a != '' and b != '':
                html = f'<h1>c = {math.sqrt(a ** 2 + b ** 2)}</h1>'
            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """
            return html

        @app.route('/calculator/surface_area')
        def calc_surface_area():
            return render_template('surface_areas.html')

        @app.route('/calculator/surface_area/cube')
        def calculate_cube():
            return render_template('cube.html')

        @app.route('/calculator/surface_area/rectangular_prism')
        def calculate_rectangle():
            return render_template('rectangular_prism.html')

        @app.route('/calculator/surface_area/shpere')
        def calculate_sphere():
            return render_template('shpere.html')

        @app.route('/calculator/surface_area/сylinder')
        def calculate_cylinder():
            return render_template('cylinder.html')

        @app.route('/calculator/surface_area/сube/calculate_it')
        def cube_c():
            s = int(request.args.get('s', None))
            html = ''
            if s != '':
                html = f'<h1>Surface Area = {6 * s}</h1>'
                html += f'<h1>Volume = {s ** 3}</h1>'
            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """
            return html

        @app.route('/calculator/surface_area/rectangular_prism/calculate_it')
        def rectangle_c():
            l = int(request.args.get('l', None))
            h = int(request.args.get('h', None))
            w = int(request.args.get('w', None))
            html = ''
            if l != '' and h != '' and w != 0:
                html = f'<h1>Surface Area = {2 * (l * w + l * h + h * w)}</h1>'
                html += f'<h1>Volume = {l * h * w}</h1>'
            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """
            return html

        @app.route('/calculator/surface_area/shpere/calculate_it')
        def sphere_c():
            r = int(request.args.get('r', None))
            pi = 3.14
            html = ''
            if r != '':
                html += f'<h1>Surface Area = {4 * pi * r ** 2}</h1>'
                html += f'<h1>Volume = {4 / 3 * pi * r ** 3}</h1>'
            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """
            return html

        @app.route('/calculator/surface_area/сylinder/calculate_it')
        def cylinder_c():
            r = int(request.args.get('r', None))
            h = int(request.args.get('h', None))
            pi = 3.14
            html = ''

            if r != '' and h != '':
                html = f'<h1>Surface Area = {(2 * r * pi) * h + 2 * r ** 2 * pi}</h1>'
                html += f'<h1>Volume = {(r ** 2 * pi) * h}</h1>'

            html += """
            <form action="/" method="get">
                <button>Вернутся на главную строничу!</button>
            </form>
            """
            return html
