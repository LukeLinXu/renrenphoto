from scrapy.item import Item, Field


class RenRenImage(Item):

    image_urls = Field()
    images = Field()
    albumId = Field()
    photoId = Field()
    ownerId = Field()
