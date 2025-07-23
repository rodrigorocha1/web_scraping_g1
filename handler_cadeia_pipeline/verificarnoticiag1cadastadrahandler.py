from handler_cadeia_pipeline.handler import Handler
from servicos.s_api.inoticia_api import INoticiaApi


class VerificarNoticiaCadastradaHandler(Handler):
    def __init__(self, api_noticia: INoticiaApi):
        super().__init__()
        self._api_noticia