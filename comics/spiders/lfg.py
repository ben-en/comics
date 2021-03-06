# coding: utf-8
from os.path import exists
from urlparse import urljoin
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from comics.utils import remove_disallowed_filename_chars, download


class LFGSpider(CrawlSpider):
    PATH = 'Archive/LookingForGroup'
    name = 'lfg'
    start_urls = ['http://www.lfg.co/archives/', ]
    allowed_domains = ['www.lfg.co', ]
    rules = (
        Rule(SgmlLinkExtractor(allow=(r'/archives/\d+/$',)), follow=True),
        Rule(SgmlLinkExtractor(allow=(r'/page/.+/$',)), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        base_url = get_base_url(response)
        no = response.url.rsplit('/')[-2]
        image_url = sel.xpath('//div[@id="comic"]/img/@src').extract()[0]
        image_url = urljoin(base_url, image_url)
        _, ext = image_url.split('/')[-1].rsplit('.', 1)
        image_name = u'{}.{}'.format(no, ext)
        path = self.PATH + '/' + remove_disallowed_filename_chars(image_name)
        if not exists(path):
            return download(image_url, path)
