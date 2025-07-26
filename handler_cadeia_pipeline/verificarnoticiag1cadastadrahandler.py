import hashlib

from click import Tuple

from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.handler import Handler
from servicos.s_api.inoticia_api import INoticiaApi


class VerificarNoticiaCadastradaHandler(Handler):
    def __init__(self, api_noticia: INoticiaApi):
        super().__init__()
        self._api_noticia = api_noticia

    def executar_processo(self, context: PipelineContext) -> bool:
        try:
            for url in context.noticia_g1:

                id_noticia = hashlib.md5(url[0].encode('utf-8')).hexdigest()
                id_noticia_api = self._api_noticia.consultar_dados_id(id_noticia=id_noticia)
                if not isinstance(id_noticia_api, Tuple):
                    context.noticia_g1_nao_cadastrada.append(url)
                return True

            return False
        except Exception:
            return False
