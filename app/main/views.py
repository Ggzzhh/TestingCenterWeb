# -*- coding: utf-8 -*-
from flask import url_for, render_template, redirect, jsonify, request

from . import main


@main.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


@main.route('/upload', methods=["POST", "GET"])
def upload():
    data = request.files
    print(data)
    json_data = {
        'errno': 0,
        'data': []
    }
    return jsonify(json_data)