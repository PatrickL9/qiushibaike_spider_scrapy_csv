# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class QiushibaikespiderPipeline:
    def process_item(self, item, spider):
        item['content'] = str(item['content']).strip()
        item['author'] = str(item['author']).strip()
        item['stat_time'] = str(item['stat_time']).strip()
        return item
