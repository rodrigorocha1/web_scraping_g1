import hashlib
import uuid
from fastapi import FastAPI, HTTPException, status, Header
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

# Sessões ativas (simples, em memória)
SESSOES_ATIVAS = {}

# Função para gerar ID único
def gerar_id_noticia(url: str) -> str:
    texto = f"{url}"
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()[:32]

# ORM - Notícias
class NoticiaDB(Base):
    __tablename__ = "noticias"
    id_noticia = Column(String(64), unique=True, primary_key=True, index=True, nullable=False)
    titulo = Column(String(255), nullable=False)
    subtitulo = Column(String(255), nullable=True)
    texto = Column(Text, nullable=False)
    autor = Column(String(100), nullable=True)
    data_hora = Column(DateTime, nullable=False)

# ORM - Usuários
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(128), nullable=False)

Base.metadata.create_all(bind=engine)

# Funções de senha
def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def verificar_senha(senha: str, senha_hash: str) -> bool:
    return gerar_hash_senha(senha) == senha_hash

# Pydantic - Entrada
class NoticiaInput(BaseModel):
    titulo_noticia: str
    url: str
    url_imagem: Optional[str] = None
    data_publicacao: Optional[datetime] = None
    descricao_noticia: Optional[str] = None
    subtitulo: Optional[str] = None
    texto_noticia: Optional[str] = None
    autor: Optional[str] = None

class UsuarioInput(BaseModel):
    username: str
    senha: str

# Pydantic - Saída
class NoticiaResponse(BaseModel):
    id_noticia: str
    titulo: str
    subtitulo: Optional[str]
    texto: str
    autor: Optional[str]
    data_hora: datetime
    class Config:
        orm_mode = True

class LoginResponse(BaseModel):
    message: str
    username: str
    token: str

app = FastAPI(title="API de Notícias com Autenticação", version="1.0.0")

# Middleware simples para verificar token
def verificar_token(authorization: str):
    if not authorization or authorization not in SESSOES_ATIVAS:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")

# ✅ Health Check
@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except OperationalError:
        raise HTTPException(status_code=500, detail="Falha na conexão com o banco de dados")

# ✅ Criar usuário
@app.post("/usuarios")
def criar_usuario(usuario: UsuarioInput):
    db = SessionLocal()
    try:
        if db.query(UsuarioDB).filter_by(username=usuario.username).first():
            raise HTTPException(status_code=400, detail="Usuário já existe")
        novo_usuario = UsuarioDB(username=usuario.username, senha_hash=gerar_hash_senha(usuario.senha))
        db.add(novo_usuario)
        db.commit()
        return {"message": "Usuário criado com sucesso", "username": usuario.username}
    finally:
        db.close()

# ✅ Login (gera token)
@app.post("/login", response_model=LoginResponse)
def login(usuario: UsuarioInput):
    db = SessionLocal()
    try:
        user_db = db.query(UsuarioDB).filter_by(username=usuario.username).first()
        if not user_db or not verificar_senha(usuario.senha, user_db.senha_hash):
            raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
        token = str(uuid.uuid4())
        SESSOES_ATIVAS[token] = usuario.username
        return {"message": "Login realizado com sucesso", "username": usuario.username, "token": token}
    finally:
        db.close()

# ✅ Criar notícia (Protegido)
@app.post("/noticias", response_model=NoticiaResponse)
def criar_noticia(noticia: NoticiaInput, Authorization: str = Header(None)):
    verificar_token(Authorization)
    db = SessionLocal()
    try:
        id_noticia = gerar_id_noticia(noticia.url)
        if db.query(NoticiaDB).filter_by(id_noticia=id_noticia).first():
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
    finally:
        db.close()

# ✅ Listar notícias (Protegido)
@app.get("/noticias", response_model=List[NoticiaResponse])
def listar_noticias(skip: int = 0, limit: int = 10, Authorization: str = Header(None)):
    verificar_token(Authorization)
    db = SessionLocal()
    try:
        return db.query(NoticiaDB).offset(skip).limit(limit).all()
    finally:
        db.close()

# ✅ Buscar notícia por ID (Protegido)
@app.get("/noticias/{id_noticia}", response_model=NoticiaResponse)
def buscar_noticia_por_id(id_noticia: str, Authorization: str = Header(None)):
    verificar_token(Authorization)
    db = SessionLocal()
    try:
        noticia = db.query(NoticiaDB).filter(NoticiaDB.id_noticia == id_noticia).first()
        if not noticia:
            raise HTTPException(status_code=404, detail="Notícia não encontrada")
        return noticia
    finally:
        db.close()
