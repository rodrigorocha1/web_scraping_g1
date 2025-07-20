from typing import TypeVar, Generic, Generator, Dict, Any

from bs4 import BeautifulSoup

from models.noticia import Noticia
from servicos.extracao.iwebscrapingbase import IWebScapingBase
from servicos.extracao.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.extracao.webscrapingsiteg1 import WebScrapingG1

T1 = TypeVar("T1")  # Tipo para conteúdo do RSS (ex.: BeautifulSoup)
R1 = TypeVar("R1")  # Tipo de retorno do RSS (ex.: Generator[Dict])
T2 = TypeVar("T2")  # Tipo para conteúdo do site G1 (ex.: BeautifulSoup)
R2 = TypeVar("R2")  # Tipo de retorno do site G1 (ex.: Noticia)


class WebScrapingPipeline(Generic[T1, R1, T2, R2]):
    def __init__(
            self,
            servico_web_scraping_rss: IWebScapingBase[T1, R1],
            servico_web_scraping_g1: IWebScapingBase[T2, R2],
    ):
        self._servico_web_scraping_rss: IWebScapingBase[T1, R1] = servico_web_scraping_rss
        self._servico_web_scraping_g1: IWebScapingBase[T2, R2] = servico_web_scraping_g1

    def rodar_web_scraping(self) -> None:

        dados_rss: T1 = self._servico_web_scraping_rss.abrir_conexao()
        rss_result: R1 = self._servico_web_scraping_rss.obter_dados(dados=dados_rss)

        if isinstance(rss_result, Generator):
            for noticia in rss_result:
                self._servico_web_scraping_g1.url = noticia["url_rss"]
                dados_g1: T2 = self._servico_web_scraping_g1.abrir_conexao()
                noticia_site: R2 = self._servico_web_scraping_g1.obter_dados(dados=dados_g1)
                print(noticia_site)
                break
        else:
            print('Não é um gerador')


if __name__ == '__main__':
    rss_service = WebScrapingBs4G1Rss(
        url="https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca"
    )

    g1_service = WebScrapingG1(
        url=None,
        parse="html.parser"
    )

    pipeline = WebScrapingPipeline[
        BeautifulSoup, Generator[Dict[str, Any], None, None],  # Tipos do RSS
        BeautifulSoup, Noticia  # Tipos do Site G1
    ](
        servico_web_scraping_rss=rss_service,
        servico_web_scraping_g1=g1_service,
    )

    pipeline.rodar_web_scraping()
