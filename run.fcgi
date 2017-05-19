#!/usr/bin/env python3.6

from os import chdir
from os.path import dirname
from sys import path

RELATIVE_WEB_URL_PATH = '/'

path.insert(0, dirname(__file__))
chdir(dirname(__file__))

from flipflop import WSGIServer
from manage import app


class ScriptNamePatch(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = RELATIVE_WEB_URL_PATH
        return self.app(environ, start_response)


app = ScriptNamePatch(app)

if __name__ == '__main__':
    WSGIServer(app).run()
