from typing import Optional, Generic, TypeVar, List, Tuple
from models.noticia import Noticia
from servicos.s_api.inoticia_api import INoticiaApi

R1 = TypeVar('R1')


class PipelineContext(Generic[R1]):

    def __init__(self, api: INoticiaApi, noticia: Noticia):
        self.api = api
        self.rss: Optional[R1] = None
        self.url_noticia_nao_cadastrada: Noticia = noticia
        self.url_noticia_g1: List[Tuple[str, Noticia]] = []
