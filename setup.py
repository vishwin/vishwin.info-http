from setuptools import setup, find_packages

setup(
	name='vishwin-http',
	version='17.05.09',
	description='The vishwin.info HTTP interface',
	url='https://git.vishwin.info/site/http.git/',
	author='Charlie Li',
	license='MPL-2.0',
	packages=find_packages(),
	install_requires=['Flask', 'markdown', 'slimit', 'Pillow', 'exifread', 'pylibmc'],
	setup_requires=['libsass>=0.6.0'],
	sass_manifests={'vishwin_http': ('scss', 'generated/css', 'static/css')},
	include_package_data=True,
	zip_safe=False
)
