from typing import TypeVar, Generic

from bs4 import BeautifulSoup

from servicos.iwebscrapingbase import IWebScapingBase
from servicos.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.webscrapingsiteg1 import WebScrapingG1

T = TypeVar("T")


class WebScrapingPipeline(Generic[T]):
    def __init__(
            self, servico_web_scraping_rss: IWebScapingBase[T],
            servico_web_scraping_g1: IWebScapingBase[T]
    ):
        self._servico_web_scraping_rss = servico_web_scraping_rss
        self._servico_web_scraping_g1 = servico_web_scraping_g1
        self._sevico_arquivo = None

    def rodar_web_scraping(self):
        dados = self._servico_web_scraping_rss.abrir_conexao()
        for noticia in self._servico_web_scraping_rss.obter_dados(dados=dados):

            print(noticia)
            self._servico_web_scraping_g1.url = noticia.url
            dados_notica_g1 = self._servico_web_scraping_g1.abrir_conexao()
            for noticia_site in self._servico_web_scraping_g1.obter_dados(dados=dados_notica_g1):
                print(noticia_site)
            print('=' * 20)


if __name__ == '__main__':
    wsp = WebScrapingPipeline[BeautifulSoup](
        servico_web_scraping_rss=WebScrapingBs4G1Rss(
            url='https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca'
        ),
        servico_web_scraping_g1=WebScrapingG1(
            url=None,
            parse='html.parser'
        )

    )

    wsp.rodar_web_scraping()
