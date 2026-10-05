from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models

# ---------- Configurações ----------
SECRET_KEY = "raizes-do-nordeste-chave-secreta-troque-em-producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------- Hash de senha ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Esquema de autenticação ----------
# HTTPBearer faz o Swagger mostrar um único campo pedindo o token
bearer_scheme = HTTPBearer()


# ---------- Dependência do banco ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Funções de hash ----------
def hash_senha(senha: str) -> str:
    """Gera hash bcrypt da senha."""
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash."""
    return pwd_context.verify(senha, senha_hash)


# ---------- Funções de token ----------
def criar_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> models.Usuario:
    """Decodifica o token Bearer e retorna o usuário logado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials  # extrai o token do header "Bearer xxx"
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception
    return usuario


def exigir_perfil(*perfis_permitidos: str):
    """Cria uma dependência que exige que o usuário tenha um dos perfis."""
    def verificador(usuario: models.Usuario = Depends(get_usuario_atual)):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Perfis permitidos: {perfis_permitidos}"
            )
        return usuario
    return verificador