# V Connect
  
### Sistema de Prestação de Contas - Compassion

Este projeto tem como objetivo facilitar e automatizar partes do processo de prestação de contas à **Compassion**. A aplicação é composta por duas partes:

- **Client (Desktop App)**: Uma aplicação de desktop construída com **Tauri** e **React**.
- **Server (API)**: Uma API desenvolvida em Flask para processar e servir os dados.

## 🧩 Estrutura do Projeto

```
V-Connect/
├── client/          # Aplicação desktop (Tauri + React)  
│   │
│   ├── src-tauri/    # Configurações do Tauri
│   │   
│   └── src/          # Construção da interface (Vite)          
│
├── server/          # API backend (Flask)
│
└──  README.md       # Este arquivo
```

## 🚀 Funcionalidades

- Upload e processamento de arquivos de prestação de contas.
- Conversão automática de dados para o formato exigido pela Compassion.
- Interface amigável para revisão e exportação dos dados.
- Backend com endpoints dedicados para processamento e validações.

## 🖥️ Como rodar o projeto

### 🔧 Pré-requisitos

- Node.js (recomendado: v18+)
- Rust (necessário para o Tauri)
- Python (recomendado: 3.10+)
- Gerenciador de pacotes (npm/yarn/pip)
- Virtualenv (opcional, mas recomendado)

### 1. Rodando o Client (Tauri + React)

```
cd client
npm install
npm run tauri dev
```

### 2. Rodando o Server (Flask API)

```bash
cd server
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run # Ou python run.py
```

Por padrão, a API roda em `http://127.0.0.1:5000`.

## 🛠️ Tecnologias Utilizadas

### Frontend (Client)
- Tauri
- React
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI

### Backend (Server)
- Python
- Flask
- Pandas (para manipulação de dados)
- Cerberus (para validação de dados)
- Flasgger (documentação da api com swagger)
- Pytest (para testes)

## 📄 Licença

Este é um projeto **privado**. Todos os direitos são reservados.

O uso, reprodução, distribuição ou modificação deste software, no todo ou em parte, é **estritamente proibido** sem autorização expressa e por escrito dos autores.

Para mais informações, entre em contato com os mantenedores do projeto.
