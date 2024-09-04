from setuptools import setup, find_packages

setup(
	name='ttsmaker',
	version='0.1',
	description='A Python library for interacting with TTSMaker API',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	author='Yosef',
	author_email='williamxhero@gmail.com',
	url='https://github.com/williamxhero/ttsmaker',
	packages=find_packages(),
	install_requires=[
		'requests',
	],
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	python_requires='>=3.11',
)