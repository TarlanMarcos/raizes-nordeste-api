# API Raízes do Nordeste

API Back-end do projeto multidisciplinar da rede de lanchonetes Raízes do Nordeste.

## Tecnologias

- Python 3
- FastAPI
- SQLAlchemy
- SQLite
- JWT (em breve)

## Como rodar

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
   pip install "fastapi[standard]" sqlalchemy
   ```

4. Rode a API:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação:
   - Swagger: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Endpoints implementados

### Lojas
- `POST /lojas` — criar loja
- `GET /lojas` — listar lojas

### Produtos
- `POST /produtos` — criar produto
- `GET /produtos` — listar produtos (com filtro opcional por `loja_id`)

### Pedidos
- `POST /pedidos` — criar pedido
- `GET /pedidos` — listar pedidos (com filtro opcional por `canal_pedido`)
- `GET /pedidos/{id}` — buscar pedido por ID

### Pagamentos
- `POST /pagamentos/{pedido_id}` — processar pagamento (mock)

## Fluxo principal

1. Criar uma loja
2. Criar um pedido vinculado a essa loja
3. Processar o pagamento (mock)
4. Consultar o pedido com o status atualizado

## Coleção Postman

O arquivo `postman_collection.json` contém todos os cenários de teste da API:

- Autenticação (registro, login, perfil)
- Lojas (criar, listar)
- Produtos (criar, listar)
- Pedidos (criar, listar, buscar)
- Pagamentos (aprovado, negado)
- Erros (401, 404, 409, 422)

### Como usar

1. Abra o Postman
2. Clique em **Import** e selecione `postman_collection.json`
3. Crie um ambiente com a variável `base_url = http://127.0.0.1:8000`
4. Rode as requisições na ordem (comece por **Login ADMIN**)

## Autor

Tarlan Marcos Dalla Vecchia