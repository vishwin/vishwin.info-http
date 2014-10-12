#!/usr/bin/python3.4
from flask import Flask, render_template, url_for, Markup
from flask.ext.libsass import *
import pkg_resources
import markdown

app=Flask(__name__)

Sass(
	{'app': 'scss/app.scss'},
	app,
	url_path='/static/css',
	include_paths=[pkg_resources.resource_filename('views', 'scss')],
	output_style='compressed'
)

@app.route('/<page>')
def get_page(page):
	md=open(pkg_resources.resource_filename('views', 'pages/' + page + '.md'), encoding='UTF-8')
	html=Markup(markdown.markdown(md.read(), output_format='html5'))
	md.close()
	if page=='index':
		return render_template('page.html', content=html)
	return render_template('page.html', content=html, title=page)

@app.route('/')
def index():
	return get_page('index')

if __name__=='__main__':
	app.run()
