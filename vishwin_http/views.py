#!/usr/bin/python3
from flask import Flask, render_template, Response, url_for, Markup, abort, send_file
from flask.ext.libsass import *
import pkg_resources

import markdown
from markdown.extensions.headerid import HeaderIdExtension

from slimit import minify

from PIL import Image
import exifread
from mimetypes import guess_type
import io

from vishwin_http import app

Sass(
	{'app': 'scss/app.scss', 'bsod': 'scss/bsod.scss'},
	app,
	url_path='/static/css',
	include_paths=[pkg_resources.resource_filename('vishwin_http.views', 'scss')],
	output_style='compressed'
)

@app.errorhandler(404)
def error_404(error):
	return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
	return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(error):
	return render_template('500.html'), 500

@app.route('/static/js/<js>')
def render_js(js):
	try:
		fd=open(pkg_resources.resource_filename('vishwin_http.views', 'js/' + js), encoding='UTF-8')
		out=minify(fd.read(), mangle=True, mangle_toplevel=True)
		fd.close()
		return Response(response=out, mimetype='text/javascript')
	except OSError:
		abort(404)

@app.route('/static/img/<imgfile>')
def return_img(imgfile):
	try:
		return send_file(pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile), mimetype=guess_type(pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile))[0])
	except OSError:
		abort(404)

@app.route('/static/img/<width>px-<imgfile>')
def render_thumb(width, imgfile):
	try:
		img=open(pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile), 'rb')
		tags=exifread.process_file(img, details=False, stop_tag='Image Orientation')
		img.close()
		img=Image.open(pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile))
		format=img.format # attribute is cleared upon transpose
		if 'Image Orientation' in tags: # really if EXIF tags are present
			if tags['Image Orientation'].values[0]>=5:
				img=img.transpose(Image.ROTATE_270) # rotations in PIL(low) are anti-clockwise, would be easier if clockwise was default
			if (tags['Image Orientation'].values[0]==(3 or 4)) or tags['Image Orientation'].values[0]>=7:
				img=img.transpose(Image.ROTATE_180)
			if tags['Image Orientation'].values[0]==(2 or 4 or 5 or 7): # flipped images
				img=img.transpose(Image.FLIP_LEFT_RIGHT)
		imgIO=io.BytesIO()
		img.thumbnail((int(width), int(width)/(img.size[0]/img.size[1])))
		img.save(imgIO, format)
		img.close()
		imgIO.seek(0)
		return send_file(imgIO, mimetype=guess_type(pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile))[0])
	except OSError:
		abort(404)

@app.route('/<page>')
def get_page(page):
	try:
		md=open(pkg_resources.resource_filename('vishwin_http.views', 'pages/' + page + '.md'), encoding='UTF-8')
		html=Markup(markdown.markdown(md.read(), output_format='html5', extensions=['markdown.extensions.attr_list', 'markdown.extensions.def_list', 'markdown.extensions.fenced_code', 'markdown.extensions.tables', 'markdown.extensions.toc', HeaderIdExtension(level=2)]))
		md.close()
		if page=='index':
			return render_template('page.html', content=html)
		return render_template('page.html', content=html, title=page)
	except OSError:
		abort(404)

@app.route('/')
def index():
	return get_page('index')
