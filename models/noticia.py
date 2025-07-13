from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Noticia:
    titulo_noticia: str
    url: str = field(compare=False)
    descricao_noticia: str
    data_publicacao: datetime
    url_imagem: str
    titulo: Optional[str] = None
    subtitulo: Optional[str] = None
    autor: Optional[str] = None
