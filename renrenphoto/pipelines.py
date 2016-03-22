import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        return request.meta['pathinfo']+super(MyImagesPipeline, self).file_path(request, response, info)

    def get_media_requests(self, item, info):
        return [Request(x, meta={'pathinfo' : item['ownerId']+'/'+item['albumId']+'/'}) for x in item.get(self.IMAGES_URLS_FIELD, [])]

