from setuptools import setup, find_packages

setup(
	name='vishwin-http',
	description='The vishwin.info HTTP interface',
	version='17.05.09',
	packages=find_packages(),
	install_requires=['Flask', 'markdown', 'slimit', 'Pillow', 'exifread', 'pylibmc'],
	setup_requires=['libsass>=0.6.0'],
	sass_manifests={'vishwin_http': ('sass', 'generated/css', 'static/css')},
	include_package_data=True,
	zip_safe=False
)
