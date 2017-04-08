#!/usr/bin/env python3
from sys import argv
from flask import Flask
import shouty


app = Flask(__name__)


@app.route('/')
def root():
    params = {
        'user': 'source',
        'password': 'hackme',
        'format': shouty.Format.MP3,
        'mount': '/shouty'
    }
    with shouty.connect(**params) as connection:
        print('Steaming')
        for file_name in argv[1:]:
            connection.send_file(file_name)


app.run(debug=True)
