# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import render_template, Response, Markup, abort, send_file
from flask_libsass import *
import pkg_resources

import markdown
from markdown.extensions.headerid import HeaderIdExtension

from slimit import minify

from PIL import Image
import exifread
from mimetypes import guess_type
import io, os.path

from vishwin_http import app, cache

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
		out=cache.get(js)
		if out is None:
			fd=open(pkg_resources.resource_filename('vishwin_http.views', 'js/' + js), encoding='UTF-8')
			out=minify(fd.read(), mangle=True, mangle_toplevel=True)
			fd.close()
			cache.set(js, out)
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
		imgpath=pkg_resources.resource_filename('vishwin_http.views', 'img/' + imgfile)
		thumbfile=width + 'px-' + imgfile
		thumbpath=pkg_resources.resource_filename('vishwin_http.views', 'img/thumb/' + thumbfile)
		# get file modified time for original; will throw exception if not found
		mtime_orig=os.path.getmtime(imgpath)
		if not (os.path.isfile(thumbpath)) or (os.path.getmtime(thumbpath) < mtime_orig):
			img=open(imgpath, 'rb')
			tags=exifread.process_file(img, details=False, stop_tag='Image_Orientation')
			img.close()
			# reopen using PIL
			img=Image.open(imgpath)
			# upon transpose, format attribute in object is cleared
			format=img.format
			if 'Image Orientation' in tags:
				if tags['Image Orientation'].values[0]>=5:
					# rotations in PIL(low) are anti-clockwise, would be easier if clockwise was default
					img=img.transpose(Image.ROTATE_270)
				if (tags['Image Orientation'].values[0]==(3 or 4)) or tags['Image Orientation'].values[0]>=7:
					img=img.transpose(Image.ROTATE_180)
				# flipped images
				if tags['Image Orientation'].values[0]==(2 or 4 or 5 or 7):
					img=img.transpose(Image.FLIP_LEFT_RIGHT)
			img.thumbnail((int(width), int(width)/(img.size[0]/img.size[1])))
			img.save(thumbpath, format)
			img.close()
		return send_file(thumbpath, mimetype=guess_type(imgpath)[0])
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
