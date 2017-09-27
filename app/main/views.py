# -*- coding: utf-8 -*-
from flask import url_for, render_template, redirect

from . import main


@main.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")
