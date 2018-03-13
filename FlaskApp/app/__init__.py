# -*- coding: utf-8 -*-
"""Flask application for displaying system infomation"""

from app import metadata


__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

from flask import Flask
app = Flask(__name__)
from app import view
