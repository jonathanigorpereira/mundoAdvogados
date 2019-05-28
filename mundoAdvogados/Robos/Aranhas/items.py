# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MundoAdvogados(scrapy.Item):
    Empresa = scrapy.Field()
    Endereco = scrapy.Field()
    Telefone = scrapy.Field()

    def set_all(self):
        for keys, _ in self.fields.items():
            self[keys] = 'NULL'
