#!/usr/bin/python3.4
from flask import Flask

app=Flask(__name__)
#app.config.from_object('config')

import vishwin_http.views
