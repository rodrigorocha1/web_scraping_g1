import hashlib
from typing import TypeVar, Generic, Generator, Dict, Any, Optional
from servicos.s_api.inoticia_api import INoticiaApi
from servicos.s_api.noticia_api import NoticiaAPI
from bs4 import BeautifulSoup
from servicos.manipulador.arquivo import Arquivo
from servicos.manipulador.arquivo_docx import ArquivoDOCX
from models.noticia import Noticia
from servicos.extracao.iwebscrapingbase import IWebScapingBase
from servicos.extracao.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.extracao.webscrapingsiteg1 import WebScrapingG1
from utils.log_pipeline import logger

T1 = TypeVar("T1")
R1 = TypeVar("R1")
T2 = TypeVar("T2")
R2 = TypeVar("R2")


class WebScrapingPipeline(Generic[T1, R1, T2, R2]):
    def __init__(
            self,
            servico_web_scraping_rss: IWebScapingBase[T1, R1],
            servico_web_scraping_g1: IWebScapingBase[T2, R2],
            arquivo: Arquivo,
            noticia_api: INoticiaApi
    ):
        self._servico_web_scraping_rss: IWebScapingBase[T1, R1] = servico_web_scraping_rss
        self._servico_web_scraping_g1: IWebScapingBase[T2, R2] = servico_web_scraping_g1
        self._arquivo = arquivo
        self._noticia_api = noticia_api
        self._diretorio = 'noticia/'



    def rodar_web_scraping(self) -> None:

        logger.info('Iniciando web scraping')

        if self._noticia_api.checar_conexao():
            print('Sucesso')

            dados_rss: Optional[T1] = self._servico_web_scraping_rss.abrir_conexao()
            if dados_rss is not None:
                rss_result: R1 = self._servico_web_scraping_rss.obter_dados(dados=dados_rss)
                if isinstance(rss_result, Generator):
                    for noticia in rss_result:
                        self._servico_web_scraping_g1.url = noticia["url_rss"]
                        id_noticia = hashlib.md5(noticia["url_rss"].encode('utf-8')).hexdigest()
                        id_noticia_api = self._noticia_api.consultar_dados_id(id_noticia=id_noticia)
                        if not id_noticia_api:
                            dados_g1: Optional[T2] = self._servico_web_scraping_g1.abrir_conexao()
                            if dados_g1 is not None:
                                noticia_site_g1: R2 = self._servico_web_scraping_g1.obter_dados(dados=dados_g1)
                                if isinstance(noticia_site_g1, Noticia) and noticia_site_g1.texto:
                                    nome_arquivo = ''.join(
                                        noticia['url_rss'].split('.')[-2].split('/')[-1].replace('-', '_') + '.docx'
                                    )
                                    self._arquivo.nome_arquivo = self._diretorio + nome_arquivo
                                    self._arquivo.noticia = noticia_site_g1
                                    self._arquivo.gerar_documento()
                                    self._arquivo()
                                    self._noticia_api.salvar_dados(noticia=noticia_site_g1)

                            else:
                                logger.warning(f'Noticia da url {noticia["url_rss"]} já existe na API')

                        else:
                            logger.warning(f'Noticia da url {noticia["url_rss"]} não encontrada')
            else:
                print('WArning URL rss fora do ar')
        else:
            logger.info('api fora do ar')
        logger.info('Terminou web scraping')


if __name__ == '__main__':
    if issubclass(ArquivoDOCX, Arquivo):
        print('OK')
    rss_service = WebScrapingBs4G1Rss(
        url="https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca"
    )

    g1_service = WebScrapingG1(
        url=None,
        parse="html.parser"
    )

    pipeline = WebScrapingPipeline[
        BeautifulSoup, Generator[Dict[str, Any], None, None],
        BeautifulSoup, Noticia
    ](
        servico_web_scraping_rss=rss_service,
        servico_web_scraping_g1=g1_service,
        arquivo=ArquivoDOCX(),
        noticia_api=NoticiaAPI()

    )

    pipeline.rodar_web_scraping()
