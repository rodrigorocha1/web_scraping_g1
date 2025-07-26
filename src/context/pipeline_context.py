from typing import Optional, Generic, TypeVar, List, Tuple
from src.models.noticia import Noticia
from src.servicos.s_api.inoticia_api import INoticiaApi

R1 = TypeVar('R1')


class PipelineContext(Generic[R1]):

    def __init__(self, api: INoticiaApi):
        self.api = api
        self.rss: Optional[R1] = None
        self.noticia_g1_nao_cadastrada: List[Tuple[str, Noticia]] = []
        self.noticia_g1: List[Tuple[str, Noticia]] = []
