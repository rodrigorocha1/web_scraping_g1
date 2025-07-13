from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Noticia:
    titulo_noticia: str
    url: str = field(compare=False)
    descricao_noticia: str
    data_publicacao: datetime
    url_imagem: str
