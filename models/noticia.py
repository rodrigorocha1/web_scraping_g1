from dataclasses import dataclass
from datetime import datetime


# Título, subtítulo, texto, autor, data e hora.

@dataclass
class Noticia:
    titulo: str
    subtitulo: str
    texto: str
    autor: str
    data_hora: datetime
