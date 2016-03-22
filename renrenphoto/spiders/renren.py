# -*- coding: utf-8 -*-
import json
from requests.packages import chardet
import scrapy
from scrapy.spiders import Spider
import sys
from renrenphoto.items import RenRenImage
import logging


class RenRenSpider(Spider):
    name = "renren"
    login_url = 'http://www.renren.com/ajaxLogin/login'
    email = 'xxxxxxx@xx.com',
    password = 'xxxxxxxxx'
    renren_ids = [249089136]
    logger = logging.getLogger('spam_application')

    def start_requests(self):
        self.logger = logging.getLogger('spam_application')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('spam.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        print sys.getdefaultencoding()
        return [scrapy.FormRequest(self.login_url, meta={'cookiejar': 1}, formdata = {
                            'email': self.email,
                            'password': self.password
                            }, callback=self.get_album_list)]

    def get_album_list(self, response):
        print("========get_album_list========")
        for renren_id in self.renren_ids:
            yield scrapy.Request('http://photo.renren.com/photo/'+str(renren_id)+'/albumlist/v7?showAll=1', meta={'cookiejar': response.meta['cookiejar']}, callback=self.get_album_detail)

    def get_album_detail(self, response):
        html_content = self.get_valid_response(response)
        begin = html_content.find("nx.data.photo")
        end = html_content.find("nx.data.hasHiddenAlbum", html_content.find("nx.data.photo"))
        print(begin, end)
        html_content = html_content[begin + len("nx.data.photo") + 3: end - 1]
        html_content = html_content.replace("\'", "\"")
        # print(html_content)
        d = json.loads(str(html_content))
        d = d['albumList']
        print('========ownerid is: ', d['ownerId'], 'albumCount: ', d['albumCount'])
        self.logger.info('albumCount:'+str(len(d['albumList'])))
        for site in d['albumList']:
            print("========get_album_detail========")
            photoCount = site['photoCount']
            page = 1
            print('albumName: ', site['albumName'], 'albumId: ', site['albumId'], 'photoCount: ', photoCount)
            self.logger.info('albumId:'+str(site['albumId']))
            while photoCount > 0 :
                yield scrapy.Request('http://photo.renren.com/photo/'+str(d['ownerId'])+'/album-'+str(site['albumId'])+'/bypage/ajax/v7?page='+str(page)+'&pageSize=100', meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse)
                page = page+1
                photoCount = photoCount-100


    def parse(self, response):
        html_content = self.get_valid_response(response)
        d = json.loads(str(html_content))
        items = []
        for site in d['photoList']:
            item = RenRenImage()
            item['image_urls'] = [site['url']]
            item['photoId'] = site['photoId']
            item['albumId'] = site['albumId']
            item['ownerId'] = site['ownerId']
            items.append(item)
        # site = d['photoList'][0]
        # item = RenRenImage()
        # item['image_urls'] = [site['url']]
        # item['photoId'] = site['photoId']
        # item['albumId'] = site['albumId']
        # item['ownerId'] = site['ownerId']
        # self.logger.info('getalbumId:'+str(site['albumId']))
        # items.append(item)
        return items


    def get_valid_response(self, response):
        html_content = response.body
        content_type = chardet.detect(html_content)
        print(content_type['encoding'])
        if content_type['encoding'] != "UTF-8":
            html_content = html_content.decode(content_type['encoding'])
        html_content = html_content.encode("utf-8")
        # open("qunima.html","wb").write(html_content)
        html_content = str(html_content)
        html_content = html_content.replace("\n", "")
        return html_content