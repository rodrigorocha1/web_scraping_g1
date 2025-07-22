from handler_cadeia_pipeline.obterrsshandler import ObterRSSHandles
from servicos.extracao.webscrapingbs4g1rss import WebScrapingBs4G1Rss
from servicos.extracao.webscrapingsiteg1 import WebScrapingG1
from servicos.manipulador.arquivo_docx import ArquivoDOCX
from servicos.s_api.noticia_api import NoticiaAPI
from handler_cadeia_pipeline.checarconexaohandler import ChecarConexaoHandler
from bs4 import BeautifulSoup
from typing import Generator, Dict, Any

rss_service = WebScrapingBs4G1Rss(url="https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca")
g1_service = WebScrapingG1(url=None, parse="html.parser")
arquivo = ArquivoDOCX()
noticia_api = NoticiaAPI()

h1 = ChecarConexaoHandler(noticia=noticia_api)
h2 = ObterRSSHandles(
    servico_webscraping=WebScrapingBs4G1Rss[
        BeautifulSoup, Generator[Dict[str, Any], None, None]
    ](url="https://g1.globo.com/rss/g1/sp/ribeirao-preto-franca")
)

h1 \
    .set_next(h2)
