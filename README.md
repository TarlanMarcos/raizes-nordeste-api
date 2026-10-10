# API Raízes do Nordeste

API Back-end do projeto multidisciplinar da rede de lanchonetes Raízes do Nordeste.

## Tecnologias usadas

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- JWT (com python-jose e passlib/bcrypt)
- Swagger/OpenAPI

## Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/TarlanMarcos/raizes-nordeste-api.git
   cd raizes-nordeste-api
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. Instale as dependências:
   ```bash
   pip install "fastapi[standard]" sqlalchemy "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
   ```

4. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação:
   - Swagger: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Endpoints disponíveis

### Autenticação
- `POST /auth/registrar` — cadastro de usuário
- `POST /auth/login` — login e geração do token JWT
- `GET /auth/me` — dados do usuário logado

### Lojas
- `POST /lojas` — criar loja (só ADMIN ou GERENTE)
- `GET /lojas` — listar lojas (público)

### Produtos
- `POST /produtos` — criar produto (só ADMIN ou GERENTE)
- `GET /produtos` — listar produtos, com filtro opcional por loja

### Pedidos
- `POST /pedidos` — criar pedido (precisa estar logado)
- `GET /pedidos` — listar pedidos, com filtro por canal
- `GET /pedidos/{id}` — buscar pedido pelo ID

### Pagamentos
- `POST /pagamentos/{pedido_id}` — processar pagamento (mock)

## Como testar o fluxo principal

1. Registrar um usuário com perfil ADMIN
2. Fazer login e copiar o token JWT
3. Clicar em "Authorize" no Swagger e colar o token
4. Criar uma loja
5. Criar um pedido vinculado a essa loja
6. Processar o pagamento (mock)
7. Consultar o pedido para ver o status atualizado

## Coleção Postman

O arquivo `postman_collection.json` reúne todos os cenários de teste da API. Ele cobre:

- Autenticação (registro, login, perfil)
- Lojas (criar, listar)
- Produtos (criar, listar)
- Pedidos (criar, listar, buscar)
- Pagamentos (aprovado, negado)
- Casos de erro (401, 403, 404, 409, 422)

**Como usar:**

1. Abra o Postman
2. Importe o arquivo `postman_collection.json`
3. Crie um ambiente com a variável `base_url = http://127.0.0.1:8000`
4. Comece pelas requisições de **Login ADMIN**, na ordem em que aparecem

## Documentação completa

O PDF do projeto está disponível no arquivo `4896093_Projeto_Back_End.pdf`.

## Autor

Tarlan Marcos Dalla Vecchia