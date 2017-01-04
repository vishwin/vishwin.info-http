# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from werkzeug.contrib.cache import FileSystemCache
import pkg_resources

app=Flask(__name__)
#app.config.from_object('config')

cache=FileSystemCache(pkg_resources.resource_filename('vishwin_http', 'cache'), default_timeout=60 * 60) # one hour timeout

import vishwin_http.views
