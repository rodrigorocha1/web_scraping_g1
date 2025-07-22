from typing import Optional, Iterable, Dict, Any
from models.noticia import Noticia
from servicos.s_api.inoticia_api import INoticiaApi

class PipelineContext:

    def __init__(self, api: INoticiaApi):
        self.api = api
        self.rss : Optional[Iterable[Dict[str, Any]]] = None
        self.noticia: Optional[Dict[str, Any]] = None
        self.noticia_site: Optional[Noticia] = None