# Scrapy settings for dirbot project
from renrenphoto import pipelines
from renrenphoto.pipelines import MyImagesPipeline

SPIDER_MODULES = ['renrenphoto.spiders']
NEWSPIDER_MODULE = 'renrenphoto.spiders'
DEFAULT_ITEM_CLASS = 'renrenphoto.items.Website'

IMAGES_STORE = 'C:/Users/llin/PycharmProjects/renrenphoto'
ITEM_PIPELINES = {'renrenphoto.pipelines.MyImagesPipeline': 1}
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"