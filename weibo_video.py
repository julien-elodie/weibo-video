#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sina_login import Weibologin as login
from bs4 import BeautifulSoup
from urllib import unquote
import os
import requests
import time
import json

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
        self.end_id = 0
        # self.totalNumber = 0

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

    def getVideos(self):
        for item in self.categories.keys():
            self.item = item
            url = self.categories[item]
            types = url.split('/')[-1]
            pageNumber = 1
            videoNumber = 0
            self.autoLoad(types, pageNumber, videoNumber)

    def autoLoad(self, types, pageNumber, videoNumber):
        while videoNumber <= 100:
            if pageNumber == 1:
                pageNumber = pageNumber + 1
                url = 'http://weibo.com/tv/' + types
                res = login.session.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.body.div.find(class_='weibo_tv_frame')
                videos = items.ul.find_all('a')
                for video in videos:
                    videoNumber = videoNumber + 1
                    href = video.get('href')
                    name = video.li.find(class_='intra_a').find(
                        class_='txt_cut').get_text()
                    url = 'http://weibo.com' + href
                    self.end_id = video.get('mid')
                    self.getVideoUrl(url, name)
            else:
                end_id = self.end_id
                __rnd = int(round(time.time()))
                url = 'http://weibo.com/p/aj/v6/mblog/videolist?type=' + \
                    types + '&page=' + \
                    str(pageNumber) + '&end_id=' + \
                    end_id + '&__rnd=' + str(__rnd)
                pageNumber = pageNumber + 1
                res = login.session.get(url)
                text = json.loads(res.text)['data']['data']
                soup = BeautifulSoup(text, 'html.parser')
                videos = soup.find_all('a')
                for video in videos:
                    videoNumber = videoNumber + 1
                    href = video.get('href')
                    name = video.li.find(class_='intra_a').find(
                        class_='txt_cut').get_text()
                    url = 'http://weibo.com' + href
                    self.end_id = video.get('mid')
                    self.getVideoUrl(url, name)

    def getVideoUrl(self, url, name):
        res = login.session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        items = soup.body.div.find(class_='weibo_player_wrap')
        href = items.div.div.get('action-data').split('&')[5]
        href = 'http:' + unquote(href.split('=')[1])
        self.videos[url] = [name, href]
        self.categories[self.item] = self.videos
        filedir = dir + self.item + '/'
        filename = name[0:17] + '.mp4'
        self.videoDownload(href, filedir, filename)
        # self.totalNumber = self.totalNumber+1
        # print self.totalNumber

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

    def simpleDownload(self):
        self.getCategries()
        self.getVideos()


download = Videodownload()
download.simpleDownload()
