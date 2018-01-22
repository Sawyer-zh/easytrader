# coding: utf8

import os
import requests
import random
from .webtrader import WebTrader
from .webtrader import NotLoginError


class DFCFTrader(WebTrader):
    config_path = os.path.dirname(__file__) + '/config/dfcf.json'

    '''初始化'''

    def __init__(self):
        self.session = requests.Session()
        super(DFCFTrader, self).__init__(debug=False)

    def _prepare_account(self, user, password, **kwargs):
        self.account_config['user'] = user
        self.account_config['password'] = password

    '''登录
        1.先获得 uuid session id  
        2.在获得验证码
        3.输入验证码 并登录
    '''

    def login(self):
        ret = self._get_uuid()
        if ret != "1":
            raise NotLoginError
        self._get_verify_code()
        identifyCode = str(input('请在程序执行目录下找到verify.png文件,并输入验证码:'))
        loginParams = {
            'userId': self.account_config['user'],
            'password': self.account_config['password'],
            'identifyCode': identifyCode,
            'randNumber': self.randNumber,
            'type': 'Z',
            'holdOnlineIdx': '1'
        }
        loginRet = self.session.post(self.config['api_login'], data=loginParams)
        if loginRet.json()['Status'] == 0:
            return True

    def _get_uuid(self):
        ret = self.session.post(self.config['api_uuid'])
        return ret.text

    def _get_verify_code(self):
        self.randNumber = random.random()
        ret = self.session.post(self.config['api_verify'] % self.randNumber)
        with open('./verify.png', 'wb') as f:
            f.write(ret.content)

    def request(self, params):
        url = self.config['prefix'] + '/' + params['controller'] + '/' + params['action']
        ret = self.session.post(url)
        return ret.json()

    def create_basic_params(self):
        return {}

    def format_response_data(self, data):
        return data