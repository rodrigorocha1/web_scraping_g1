from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.handler import Handler
from typing import TypeVar, Generic, Generator

from models.noticia import Noticia
from servicos.extracao.iwebscrapingbase import IWebScapingBase

SWB = TypeVar('SWB')
RTN = TypeVar('RTN')


class ObterUrlG1Handler(Handler, Generic[SWB, RTN]):
    def __init__(self, web_scraping_g1: IWebScapingBase[SWB, RTN]):
        super().__init__()
        self._servico_web_scraping_g1 = web_scraping_g1

    def executar_processo(self, context: PipelineContext) -> bool:
        dados_g1 = context.rss
        if isinstance(dados_g1, Generator):
            for dado in dados_g1:
                if isinstance(dado, dict) and dado['url_rss'] is not None:
                    self._servico_web_scraping_g1.url = dado['url_rss']
                    dado_g1 = self._servico_web_scraping_g1.abrir_conexao()
                    if dado_g1:
                        noticia = self._servico_web_scraping_g1.obter_dados(dados=dado_g1)
                        if isinstance(noticia, Noticia):
                            context.url_noticia_g1_nao_cadastrada.append(noticia)
            return True
        return False
