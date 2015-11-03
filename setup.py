from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="wpbiff",
    version="0.1.1",
    author="Gabor Szathmari",
    author_email="gszathmari@gmail.com",
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    include_package_data=True,
    url="https://github.com/gszathmari/wpbiff",
    license="MIT",
    platforms = ["Linux"],
    description="Wordpress Two-Factor Authentication Brute-forcer",
    long_description=long_description,
    entry_points='''
        [console_scripts]
        wpbiff=wpbiff.cli:main
    ''',
    install_requires=[
        "click",
        "colorama",
        "progressbar",
        "requests"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Security',
        'Intended Audience :: Other Audience',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='security password',
)
