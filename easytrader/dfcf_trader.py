# coding: utf8

import os
import requests
from .webtrader import WebTrader


class DFCFTrader(WebTrader):
    config_path = os.path.dirname(__file__) + '/config/dfcf.json'

    def __init__(self):
        super.__init__()

