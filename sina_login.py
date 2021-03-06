#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import json
import base64
import rsa
import binascii
from bs4 import BeautifulSoup


class Weibologin(object):
    """docstring for Weibologin."""

    def __init__(self):
        super(Weibologin, self).__init__()

    def setUsername(self, user):
        self.username = user

    def setPassword(self, passwd):
        self.password = passwd

    def showCurrentUser(self):
        print self.username

    def initSession(self):
        self.session = requests.Session()
        self.session.get('http://weibo.com/login.php')

    def getSession(self):
        return self.session

    def initPostData(self):
        self.postdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': False,
            'useticket': '1',
            'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'sr': '1366*768',
            'encoding': 'UTF-8',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META',
        }

    def setPostData(
            self,
            servertime='',
            nonce='',
            rsakv='',
            su='',
            sp=''):
        self.postdata['servertime'] = servertime
        self.postdata['nonce'] = nonce
        self.postdata['rsakv'] = rsakv
        self.postdata['su'] = su
        self.postdata['sp'] = sp

    def showPostData(self):
        print self.postdata

    def getParameters(self):
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)'
        res = self.session.get(url)
        data = re.findall(r'(?<=\().*(?=\))', res.text)[0]
        data = json.loads(data)
        return (data['servertime'], data['nonce'], data['pubkey'], data['rsakv'])

    def getSu(self):
        return base64.b64encode(self.username.encode(encoding='utf-8'))

    def getSp(self):
        pubkey = self.getParameters()[2]
        rsaPubkey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPubkey, 65537)
        message = str(self.getParameters()[
                      0]) + '\t' + str(self.getParameters()[1]) + '\n' + str(self.password)
        return binascii.b2a_hex(rsa.encrypt(message.encode(encoding='utf-8'), key))

    def getLoginUrl(self):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        res = self.session.post(url, data=self.postdata)
        return re.findall(r'https://passport.weibo.*&retcode=0',res.text)[0]

    def getPassport(self):
        url = self.getLoginUrl()
        res = self.session.get(url)
        self.passport = re.findall('"uniqueid":"(\d+)",',res.text)[0]

    def showPassport(self):
        print self.passport

    def login(self):
        url = 'http://weibo.com/u/'+self.passport
        res = self.session.get(url)
        nickname = re.findall(r'\"username\\\"\>(.*?)\<',res.text)[0]
        print 'User ' + nickname + ' login!'

    def simpleLogin(self, user='15168173848', passwd='wyq2644756656'):
        self.setUsername(user)
        self.setPassword(passwd)
        self.initSession()
        self.initPostData()
        servertime, nonce, pubkey, rsakv = self.getParameters()
        su = self.getSu()
        sp = self.getSp()
        self.setPostData(servertime=servertime,nonce=nonce,rsakv=rsakv,su=su,sp=sp)
        self.getPassport()
        self.login()
