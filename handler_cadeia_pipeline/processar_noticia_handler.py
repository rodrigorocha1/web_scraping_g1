from typing import TypeVar, Generic

from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.handler import Handler

from servicos.s_api.inoticia_api import INoticiaApi


class ProcessarNoticiaHandler(Handler):

    def __init__(self, api_noticia: INoticiaApi):
        super().__init__()
        self._api_noticia = api_noticia

    def executar_processo(self, context: PipelineContext) -> bool:
        noticia = context.noticia_g1_nao_cadastrada
        print(noticia)
        return True
