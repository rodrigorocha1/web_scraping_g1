from typing import Optional, Generic, TypeVar, List
from servicos.s_api.inoticia_api import INoticiaApi

R1 = TypeVar('R1')
R2 = TypeVar('R2')
R3 = TypeVar('R3')


class PipelineContext(Generic[R1]):

    def __init__(self, api: INoticiaApi):
        self.api = api
        self.rss: Optional[R1] = None
        self.url_noticia_nao_cadastrada: List[str] = []
        self.url_noticia_g1: List[str] = []
