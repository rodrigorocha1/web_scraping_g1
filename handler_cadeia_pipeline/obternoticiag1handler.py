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
                if isinstance(dado, dict) and dado['url_rss'] is not None:
                    self._servico_web_scraping_g1.url = dado['url_rss']
                    dados = self._servico_web_scraping_g1.abrir_conexao()

                    noticia = self._servico_web_scraping_g1.obter_dados(dados=dados)

                    context.url_noticia_g1.append((self._servico_web_scraping_g1.url, noticia))
            return True
        return False
