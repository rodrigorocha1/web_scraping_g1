from typing import Generator, Dict, Any
from bs4 import BeautifulSoup

from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.checarconexaohandler import ChecarConexaoHandler
from handler_cadeia_pipeline.obterrsshandler import ObterRSSHandler
from handler_cadeia_pipeline.obternoticiag1handler import ObterUrlG1Handler
from handler_cadeia_pipeline.verificarnoticiag1cadastadrahandler import VerificarNoticiaCadastradaHandler
from handler_cadeia_pipeline.processar_noticia_handler import ProcessarNoticiaHandler

from servicos.extracao.iwebscrapingbase import IWebScapingBase
from servicos.extracao.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.extracao.webscrapingsiteg1 import WebScrapingG1
from servicos.manipulador.arquivo import Arquivo
from servicos.manipulador.arquivo_docx import ArquivoDOCX
from servicos.s_api.inoticia_api import INoticiaApi
from servicos.s_api.noticia_api import NoticiaAPI
from models.noticia import Noticia


class FabricaPipelineHandler:

    def __init__(self, api_service: INoticiaApi, rss_service: IWebScapingBase,
                 g1_service: IWebScapingBase, arquivo_service: Arquivo):
        self.api_service = api_service
        self.rss_service = rss_service
        self.g1_service = g1_service
        self.arquivo_service = arquivo_service

    def criar_contexto(self) -> PipelineContext:
        return PipelineContext[Generator[Dict[str, Any], None, None]](api=self.api_service)

    def criar_pipeline(self) -> ChecarConexaoHandler:
        p1 = ChecarConexaoHandler(api_noticia=self.api_service)
        p2 = ObterRSSHandler[BeautifulSoup, Generator[Dict[str, Any], None, None]](
            servico_webscraping=self.rss_service
        )
        p3 = ObterUrlG1Handler[BeautifulSoup, Noticia](
            web_scraping_g1=self.g1_service
        )
        p4 = VerificarNoticiaCadastradaHandler(api_noticia=self.api_service)
        p5 = ProcessarNoticiaHandler(api_noticia=self.api_service, arquivo=self.arquivo_service)

        p1.set_next(p2).set_next(p3).set_next(p4).set_next(p5)

        return p1


if __name__ == "__main__":
    URL_RSS = "https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca"
    PARSER_HTML = "html.parser"

    rss_service = WebScrapingBs4G1Rss(url=URL_RSS)
    g1_service = WebScrapingG1(url=None, parse=PARSER_HTML)
    arquivo_service = ArquivoDOCX()
    api_service = NoticiaAPI()

    factory = FabricaPipelineHandler(
        api_service=api_service,
        rss_service=rss_service,
        g1_service=g1_service,
        arquivo_service=arquivo_service
    )

    contexto = factory.criar_contexto()
    pipeline = factory.criar_pipeline()

    pipeline.handle(contexto)
