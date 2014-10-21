#!/usr/bin/python3.4
from flask import Flask, render_template, url_for, Markup, abort
from flask.ext.libsass import *
import pkg_resources, socket

import markdown
from markdown.extensions.headerid import HeaderIdExtension

from slimit import minify

app=Flask(__name__)

Sass(
	{'app': 'scss/app.scss'},
	app,
	url_path='/static/css',
	include_paths=[pkg_resources.resource_filename('views', 'scss')],
	output_style='compressed'
)

@app.route('/static/js/<js>')
def render_js(js):
	try:
		fd=open(pkg_resources.resource_filename('views', 'js/' + js), encoding='UTF-8')
		out=minify(fd.read(), mangle=True, mangle_toplevel=True)
		fd.close()
		return out
	except OSError:
		abort(404)

@app.route('/<page>')
def get_page(page):
	try:
		md=open(pkg_resources.resource_filename('views', 'pages/' + page + '.md'), encoding='UTF-8')
		html=Markup(markdown.markdown(md.read(), output_format='html5', extensions=['markdown.extensions.attr_list', 'markdown.extensions.def_list', 'markdown.extensions.fenced_code', 'markdown.extensions.tables', 'markdown.extensions.toc', HeaderIdExtension(level=2)]))
		md.close()
		if page=='index':
			return render_template('page.html', hostname=socket.gethostname(), content=html)
		return render_template('page.html', hostname=socket.gethostname(), content=html, title=page)
	except OSError:
		abort(404)

@app.route('/')
def index():
	return get_page('index')

if __name__=='__main__':
	app.run()
