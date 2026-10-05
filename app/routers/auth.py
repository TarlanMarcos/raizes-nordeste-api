from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import (
    get_db,
    hash_senha,
    verificar_senha,
    criar_token,
    get_usuario_atual,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário com senha em hash."""
    # Verifica se email já existe
    existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado."
        )

    # Verifica consentimento LGPD
    if not usuario.consentimento_lgpd:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Consentimento LGPD é obrigatório para cadastro."
        )

    novo_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha),
        perfil=usuario.perfil,
        consentimento_lgpd=usuario.consentimento_lgpd,
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/login", response_model=schemas.TokenResponse)
def login(dados: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Autentica e retorna um token JWT."""
    usuario = db.query(models.Usuario).filter(models.Usuario.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos."
        )

    token = criar_token(
        data={"sub": usuario.email, "perfil": usuario.perfil},
        expires_delta=__import__("datetime").timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return schemas.TokenResponse(access_token=token, perfil=usuario.perfil)


@router.get("/me", response_model=schemas.UsuarioResponse)
def meu_perfil(usuario: models.Usuario = Depends(get_usuario_atual)):
    """Retorna os dados do usuário logado."""
    return usuario