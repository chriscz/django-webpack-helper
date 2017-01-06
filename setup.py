from setuptools import setup, find_packages

setup(
    name="django-webpack-helper",
    version="0.1.2",
    url="httpd://github.com/chriscz/django-webpack-helper",
    description="A django app that helps integrate webpack",
    author="Chris Coetzee",
    license='Mozilla Public License 2.0 (MPL 2.0)',
    author_email='chriscz93@gmail.com',
    packages=find_packages(include=['webpack_helper']),
    install_requires=[
        'django-webpack-loader'
    ],
    include_package_data=True,

    classifiers = [
        "Programming Language :: Python :: 2.7",            
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ]
)
