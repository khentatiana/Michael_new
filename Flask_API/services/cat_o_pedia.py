from flask import render_template, request
import sqlite3


class Cat:
    def __init__(self, app):
        @app.route('/cat_o_log')
        def main_cat_page():
            # main cat page where you can browse existing cats


