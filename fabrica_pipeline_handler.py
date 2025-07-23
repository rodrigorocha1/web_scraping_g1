from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.obternoticiag1handler import ObterUrlG1Handler
from handler_cadeia_pipeline.obterrsshandler import ObterRSSHandler
from handler_cadeia_pipeline.processar_noticia_handler import ProcessarNoticiaHandler
from handler_cadeia_pipeline.verificarnoticiag1cadastadrahandler import VerificarNoticiaCadastradaHandler
from servicos.extracao.iwebscrapingbase import IWebScapingBase
from servicos.extracao.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.extracao.webscrapingsiteg1 import WebScrapingG1
from servicos.manipulador.arquivo import Arquivo
from servicos.manipulador.arquivo_docx import ArquivoDOCX
from servicos.s_api.inoticia_api import INoticiaApi
from servicos.s_api.noticia_api import NoticiaAPI
from handler_cadeia_pipeline.checarconexaohandler import ChecarConexaoHandler
from bs4 import BeautifulSoup
from typing import Generator, Dict, Any, List, TypeVar, Generic
from models.noticia import Noticia

T1 = TypeVar("T1")
R1 = TypeVar("R1",)
T2 = TypeVar("T2")
R2 = TypeVar("R2")



class FabricaPipelineHandler(Generic[T1, R1, T2, R2]):
    def __init__(
            self, url_rss: str,
            rss_service: IWebScapingBase,
            g1_service: IWebScapingBase,
            api_service: INoticiaApi,
            arquivo_service: Arquivo,
            parser_html: str = 'html.parser',
    ):
        self.url_rss = url_rss
        self.parser_html = parser_html
        self.rss_service = rss_service
        self.g1_service = g1_service
        self.api_service = api_service
        self.arquivo_service = arquivo_service

    def criar_contexto(self) -> PipelineContext:
        return PipelineContext[Generator[Dict[str, Any], None, None]](api=NoticiaAPI())

    def criar_corrente_pipeline(self) -> ChecarConexaoHandler:
        p1 = ChecarConexaoHandler(api_noticia=self.api_service)
        p2 = ObterRSSHandler[BeautifulSoup, Generator[Dict[str, Any], None, None]](
            servico_webscraping=self.rss_service
        )
        p3 = ObterUrlG1Handler[BeautifulSoup, Noticia](web_scraping_g1=self.g1_service)
        p4 = VerificarNoticiaCadastradaHandler(api_noticia=self.api_service)
        p5 = ProcessarNoticiaHandler(api_noticia=self.api_service, arquivo=self.arquivo_service)
        p1.set_next(p2).set_next(p3).set_next(p4).set_next(p5)
        return p1


if __name__ == "__main__":
    URL_RSS = "https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca"
    rss_service = WebScrapingBs4G1Rss(url=URL_RSS)
    g1_service = WebScrapingG1(url=None, parse='html.parser')
    api_service = NoticiaAPI()
    arquivo_service = ArquivoDOCX()
    fabrica_pipeline = FabricaPipelineHandler[
        BeautifulSoup, Generator[Dict[str, Any], None, None],
        BeautifulSoup, Noticia
    ](
        url_rss=URL_RSS,
        rss_service=rss_service,
        g1_service=g1_service,
        api_service=api_service,
        arquivo_service=arquivo_service
    )
    contexto = fabrica_pipeline.criar_contexto()
    pipeline = fabrica_pipeline.criar_corrente_pipeline()
    pipeline.handle(contexto)
