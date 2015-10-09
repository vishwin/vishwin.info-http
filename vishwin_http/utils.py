#!/usr/bin/python3

def img_mimetype(ext):
	return {
		'jpg': 'image/jpeg',
		'jpe': 'image/jpeg',
		'jpeg': 'image/jpeg',
		'png': 'image/png',
		'gif': 'image/gif'
	}.get(ext, 'image/png')
