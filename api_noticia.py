import hashlib
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError, IntegrityError

# Configuração do banco SQLite
DATABASE_URL = "sqlite:///./noticias.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Função para gerar ID único
def gerar_id_noticia(url: str) -> str:
    texto = f"{url}"
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:32]  # reduzido para 32 caracteres


# Modelo ORM (Banco)
class NoticiaDB(Base):
    __tablename__ = "noticias"

    id_noticia = Column(String(64), unique=True, primary_key=True, index=True, nullable=False)
    titulo = Column(String(255), nullable=False)
    subtitulo = Column(String(255), nullable=True)
    texto = Column(Text, nullable=False)
    autor = Column(String(100), nullable=True)
    data_hora = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine)


# Modelo Pydantic (entrada)
class NoticiaInput(BaseModel):
    titulo_noticia: str
    url: str
    url_imagem: Optional[str] = None
    data_publicacao: Optional[datetime] = None
    descricao_noticia: Optional[str] = None
    subtitulo: Optional[str] = None
    texto_noticia: Optional[str] = None
    autor: Optional[str] = None


# Modelo Pydantic (resposta)
class NoticiaResponse(BaseModel):
    id_noticia: str
    titulo: str
    subtitulo: Optional[str]
    texto: str
    autor: Optional[str]
    data_hora: datetime

    class Config:
        orm_mode = True


app = FastAPI(title="API de Notícias", version="1.0.0")


# ✅ Endpoint de Health Check
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "code": status.HTTP_200_OK
        }
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha na conexão com o banco de dados"
        )

# ✅ Endpoint para criar uma notícia
@app.post("/noticias", response_model=NoticiaResponse, status_code=status.HTTP_201_CREATED)
def criar_noticia(noticia: NoticiaInput):
    db = SessionLocal()
    try:
        id_noticia = gerar_id_noticia(noticia.titulo_noticia, noticia.url)

        # Verifica se já existe no banco
        existe = db.query(NoticiaDB).filter_by(id_noticia=id_noticia).first()
        if existe:
            raise HTTPException(status_code=400, detail="Notícia já cadastrada")

        nova_noticia = NoticiaDB(
            id_noticia=id_noticia,
            titulo=noticia.titulo_noticia,
            subtitulo=noticia.subtitulo,
            texto=noticia.texto_noticia or noticia.descricao_noticia or "",
            autor=noticia.autor,
            data_hora=noticia.data_publicacao or datetime.now()
        )
        db.add(nova_noticia)
        db.commit()
        db.refresh(nova_noticia)
        return nova_noticia
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    finally:
        db.close()


# ✅ Endpoint para listar todas as notícias
@app.get("/noticias", response_model=List[NoticiaResponse], status_code=status.HTTP_200_OK)
def listar_noticias(skip: int = 0, limit: int = 10):
    db = SessionLocal()
    try:
        noticias = db.query(NoticiaDB).offset(skip).limit(limit).all()
        if not noticias:
            raise HTTPException(status_code=404, detail="Nenhuma notícia encontrada")
        return noticias
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar notícias: {str(e)}")
    finally:
        db.close()


@app.get("/noticias/{id_noticia}", response_model=NoticiaResponse, status_code=status.HTTP_200_OK)
def buscar_noticia_por_id(id_noticia: str):
    """
    Busca uma notícia pelo id_noticia (hash único).
    """
    db = SessionLocal()
    try:
        noticia = db.query(NoticiaDB).filter(NoticiaDB.id_noticia == id_noticia).first()
        if not noticia:
            raise HTTPException(status_code=404, detail="Notícia não encontrada")
        return noticia
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar notícia: {str(e)}")
    finally:
        db.close()
