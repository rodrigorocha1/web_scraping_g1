from typing import TypeVar, Generic

from context.pipeline_context import PipelineContext
from handler_cadeia_pipeline.handler import Handler
from servicos.manipulador.arquivo import Arquivo

from servicos.s_api.inoticia_api import INoticiaApi


class ProcessarNoticiaHandler(Handler):

    def __init__(self, api_noticia: INoticiaApi, arquivo: Arquivo):
        super().__init__()
        self._api_noticia = api_noticia
        self._arquivo = arquivo
        self._diretorio = 'noticia/'

    def executar_processo(self, context: PipelineContext) -> bool:
        noticias_g1 = context.noticia_g1_nao_cadastrada
        for noticia_g1 in noticias_g1:
            url_g1, noticia = noticia_g1
            nome_arquivo = ''.join(
                url_g1.split('.')[-2].split('/')[-1].replace('-', '_') + '.docx'
            )
            self._arquivo.nome_arquivo = self._diretorio + nome_arquivo
            self._arquivo.noticia = noticia
            self._arquivo.gerar_documento()
            self._arquivo()
            self._api_noticia.salvar_dados(noticia=noticia)

        return True
