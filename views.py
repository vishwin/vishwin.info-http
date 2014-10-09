#!/usr/bin/python3.4
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
	return 'Just messing around. Nothing to see yet.'

@app.route('/<page>')
def get_page(page):
	return 'This is where ' + page + ' would display.'

if __name__=='__main__':
	app.run()
