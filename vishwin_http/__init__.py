# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from werkzeug.contrib.cache import MemcachedCache
import pkg_resources

app=Flask(__name__)
app.config.from_pyfile('config.py')

# set up a memcached Werkzeug cache, prefixing each key, with default timeout of one hour
cache=MemcachedCache(servers=app.config['MEMCACHED_SERVERS'], key_prefix=app.config['MEMCACHED_KEYPREFIX'], default_timeout=60 * 60)

import vishwin_http.views
