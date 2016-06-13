#!/usr/bin/python3
from flask import Flask
from werkzeug.contrib.cache import FileSystemCache
import pkg_resources

app=Flask(__name__)
#app.config.from_object('config')

cache=FileSystemCache(pkg_resources.resource_filename('vishwin_http', 'cache'), default_timeout=60 * 60) # one hour timeout

import vishwin_http.views
