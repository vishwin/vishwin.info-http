#!/usr/bin/python3.4
from flask import Flask

app=Flask(__name__)
app.config_from_object('config')

import views
