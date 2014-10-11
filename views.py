#!/usr/bin/python3.4
from flask import Flask, render_template, url_for
from flask.ext.libsass import *
import pkg_resources

app=Flask(__name__)

Sass(
	{'app': 'scss/app.scss'},
	app,
	url_path='/static/css',
	include_paths=[pkg_resources.resource_filename('views', 'scss')],
	output_style='compressed'
)

@app.route('/')
def index():
	return 'Just messing around. Nothing to see yet.'

@app.route('/<page>')
def get_page(page):
	return 'This is where ' + page + ' would display.'

if __name__=='__main__':
	app.run()
