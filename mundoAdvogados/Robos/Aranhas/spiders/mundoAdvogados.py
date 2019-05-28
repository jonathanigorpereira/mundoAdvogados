# -*- coding: utf-8 -*-
import scrapy
from scrapy import *
from Aranhas.items import MundoAdvogados


class mundoAdvogados(scrapy.Spider):
    name = 'mundoAdvogados'
    start_urls = ['https://www.mundoadvogados.com.br/escritorios/licitacoes']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['Empresa', 'Endereco', 'Telefone'],
        'FEED_FORMAT': 'csv'
    }

    def parse(self, response):
            ultimaPagina = int(response.xpath('//*[@class="ie-pagination-block pager-module"]/span')[2].re_first('\d{2,11}'))
            for x in xrange(1, ultimaPagina,1):
                if x == 1:
                    urlPagina = 'https://www.mundoadvogados.com.br/escritorios/licitacoes'
                else:
                    urlPagina = 'https://www.mundoadvogados.com.br/escritorios/licitacoes/'+str(x)
                req = Request(url=urlPagina, callback=self.parsePagina)
                yield req

    def parsePagina(self, response):
        url_base = 'https://www.mundoadvogados.com.br'
        script = response.xpath('//a[@class="ie-listings-item-header-info-ttl bh_com_list_link"]')
        for urls in script:
            links = urls.xpath('.//@href').extract_first()
            link_completo = url_base + str(links)
            yield Request(url=link_completo, callback=self.parseAviso)

    def parseAviso(self, response):
        try:
            telefone = response.xpath('//script[@type="application/ld+json"]').re_first('telephone.*"(.*?)"')
            endereco = response.xpath('//script[@type="application/ld+json"]').re_first('streetAddress.*"(.*?)"')
            nome_empresa = response.xpath('//script[@type="application/ld+json"]').re_first('name.*"(.*?)"')

            item = MundoAdvogados()
            item.set_all()
            if "&amp;" in nome_empresa:
                empresa = nome_empresa.split('&amp;')[0]+''+nome_empresa.split('&amp;')[1]
                item['Empresa'] = empresa.encode('utf-8')
            else:
                item['Empresa'] = nome_empresa.encode('utf-8')
            item['Endereco'] = endereco.encode('utf-8')
            item['Telefone'] = telefone.strip().encode('utf-8')
            yield item
        except Exception as e:
            print 'erro no parse Aviso ' + e.message
