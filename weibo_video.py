#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sina_login import Weibologin as login
from bs4 import BeautifulSoup
import re
from urllib import unquote
import os
import requests

login = login()
login.simpleLogin()

dir = 'data/'
if not os.path.exists(dir):
    os.mkdir(dir)


class Videodownload(object):
    """docstring for Videodownload."""

    def __init__(self):
        super(Videodownload, self).__init__()
        self.categories = {}
        self.videos = {}

    def getCategries(self):
        url = 'http://weibo.com/tv'
        res = login.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.body.div.find(class_='weibo_tv_frame')
        categories = items.find_all(class_='L_ctit')
        categoryNumber = 0
        for category in categories:
            categoryNumber = categoryNumber + 1
            if categoryNumber <= 12:
                href = category.a.get('href')
                name = category.a.span.em.find_next_sibling().get_text()
                self.categories[name] = 'http://weibo.com' + href
                filedir = dir + name + '/'
                if not os.path.exists(filedir):
                    os.mkdir(filedir)

    def getVedios(self):
        for item in self.categories.keys():
            url = self.categories[item]
            res = login.session.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.body.div.find(class_='weibo_tv_frame')
            videos = items.ul.find_all('a')
            videoNumber = 0
            for video in videos:
                videoNumber = videoNumber + 1
                href = video.get('href')
                name = video.li.find(class_='intra_a').find(
                    class_='txt_cut').get_text()
                url = 'http://weibo.com' + href
                res = login.session.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.body.div.find(class_='weibo_player_wrap')
                href = items.div.div.get('action-data').split('&')[5]
                href = 'http:' + unquote(href.split('=')[1])
                self.videos[url] = [name, href]
                self.categories[item] = self.videos
                filedir = dir + item + '/'
                filename = name[0:17] + '.mp4'
                self.videoDownload(href, filedir, filename)

    def videoDownload(self, url, filedir, filename):
        print filename + u'开始下载'
        res = requests.get(url)
        with open(filedir + filename, 'wb') as code:
            code.write(res.content)
        print filename + u'下载完成'

    def showCategories(self):
        for item in self.categories.keys():
            print item
            print self.categories[item]

    def showVideos(self):
        for item in self.categories.keys():
            for lists in self.categories[item]:
                if type(self.categories[item]) == list:
                    print self.categories[item][lists][0]
                    print self.categories[item][lists][1]

    def autoLoad(self):
        // # TODO: 


download = Videodownload()
download.getCategries()
download.getVedios()
