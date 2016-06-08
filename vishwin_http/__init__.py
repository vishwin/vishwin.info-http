#!/usr/bin/python3
from flask import Flask
from werkzeug.contrib.cache import SimpleCache

app=Flask(__name__)
#app.config.from_object('config')

cache=SimpleCache()

import vishwin_http.views
