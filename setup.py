#!/usr/bin/env python

from setuptools import setup as setup, find_packages

install_require = [
	'flask',
    'nmeaserver',
	'setuptools',
    'RPi.GPIO', #Disable this line on non-RaspberryPI computers -- Also fix lines 15-16 of seven-segment.py
	#'fake_rpi', #Enable this line on non-RaspberryPI computers -- Also fix lines 15-16 of seven-segment.py
]

setup(name='seven-segment-controller',
	  version='1.1',
	  description='Control software for the 7-segment display running on a Raspberry PI.',
	  author='Felix Pageau',
	  author_email='pageau@robonation.org',
	  license='Apache License 2.0',
	  url='https://github.com/robonation/seven-segment-controller',
	  install_requires=install_require,
	  test_suite='nose.collector',
	  python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
	  packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
	  classifiers=[
		"Development Status :: 4 - Beta",
		"Intended Audience :: Science/Research",
		"License :: OSI Approved :: Apache Software License",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
	],
)
