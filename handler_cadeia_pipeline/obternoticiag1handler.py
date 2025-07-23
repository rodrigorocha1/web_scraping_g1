from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.handler import Handler
from typing import TypeVar, Generic, Generator
from servicos.extracao.iwebscrapingbase import IWebScapingBase


SWB = TypeVar('SWB')
RTN = TypeVar('RTN')


class ObterUrlG1Handler(Handler, Generic[SWB, RTN]):
    def __init__(self, web_scraping_g1: IWebScapingBase[SWB, RTN]):
        super().__init__()
        self._servico_web_scraping_g1 = web_scraping_g1


    def executar_processo(self, context: PipelineContext) -> bool:
        dados = context.rss
        if isinstance(dados, Generator):
            for dado in dados:
                if isinstance(dado, dict) and dado['url_rss'] is not None :
                    url_g1 = dado['url_rss']
                    context.url_noticia_g1.append(url_g1)

            return True
        return False
