from dataclasses import dataclass, field
from datetime import datetime
from turtle import st
from typing import Optional


@dataclass
class Noticia:
    titulo_noticia: str
    url: str
    url_imagem: Optional[str] = None
    data_publicacao: Optional[datetime] = None
    descricao_noticia: Optional[str] = None
    subtitulo: Optional[str] = None
    texto_noticia: Optional[str] = None
    autor: Optional[str] = None
