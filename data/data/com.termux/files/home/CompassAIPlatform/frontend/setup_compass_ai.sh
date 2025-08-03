export default App;

# frontend/.env
create_file_with_content "$FRONTEND_DIR/.env" 'REACT_APP_API_URL=http://localhost:8000/api/v1'

# --- Instalação de Dependências do Sistema (Termux) ---
echo ""
echo "Instalando pacotes do sistema (PostgreSQL, MongoDB, Node.js)..."
pkg update -y
pkg upgrade -y
pkg install -y postgresql mongodb nodejs

# --- Configuração e Inicialização do PostgreSQL ---
echo ""
echo "Configurando PostgreSQL..."
if [ ! -d "$PREFIX/var/lib/postgresql" ]; then
    initdb "$PREFIX/var/lib/postgresql"
fi

pg_ctl -D "$PREFIX/var/lib/postgresql" start || { echo "PostgreSQL já pode estar rodando ou houve um erro ao iniciar."; }

echo "Criando usuário e banco de dados PostgreSQL (se não existirem)..."
# Tenta criar usuário 'user' e banco de dados 'mydatabase'
# Ajuste conforme o .env.example
psql -U postgres -c "CREATE USER user WITH PASSWORD 'password';" 2>/dev/null || true
psql -U postgres -c "CREATE DATABASE mydatabase OWNER user;" 2>/dev/null || true

echo "PostgreSQL configurado. Verifique as credenciais no .env."

# --- Configuração e Inicialização do MongoDB ---
echo ""
echo "Configurando MongoDB..."
if [ ! -d "$PREFIX/var/lib/mongodb" ]; then
    mkdir -p "$PREFIX/var/lib/mongodb"
fi

# Inicia o mongod em segundo plano
nohup mongod --bind_ip 127.0.0.1 --port 27017 --dbpath "$PREFIX/var/lib/mongodb" > "$PROJECT_ROOT/mongodb_log.out" 2>&1 &

echo "MongoDB iniciado em segundo plano. Logs em: $PROJECT_ROOT/mongodb_log.out"

# --- Instalação de Dependências Python (Backend) ---
echo ""
echo "Instalando dependências Python para o backend..."
cd "$BACKEND_DIR" || { echo "Falha ao entrar no diretório do backend. Abortando."; exit 1; }

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || { echo "Falha ao instalar dependências Python. Verifique o requirements.txt."; exit 1; }
deactivate # Desativa o venv após a instalação

# --- Instalação de Dependências Node.js (Frontend) ---
echo ""
echo "Instalando dependências Node.js para o frontend..."
cd "$FRONTEND_DIR" || { echo "Falha ao entrar no diretório do frontend. Abortando."; exit 1; }
npm install || { echo "Falha ao instalar dependências Node.js. Verifique o package.json."; exit 1; }

echo ""
echo "==============================================="
echo "          Setup Concluído!"
echo "==============================================="
echo "Próximos passos:"
echo "1. Edite '$BACKEND_DIR/.env' com suas credenciais reais para PostgreSQL e MongoDB."
echo "2. Inicie o backend:"
echo "   cd $BACKEND_DIR"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo "3. Em outra sessão do Termux, inicie o frontend:"
echo "   cd $FRONTEND_DIR"
echo "   npm start"
echo ""
echo "Acesse o frontend em http://localhost:3000 (ou o IP do seu dispositivo Termux na porta 3000)."
echo "O backend estará em http://localhost:8000."
echo "Lembre-se de que o MongoDB e PostgreSQL devem estar rodando."
echo "Para parar o MongoDB, use 'pkill mongod'."
echo "Para parar o PostgreSQL, use 'pg_ctl -D $PREFIX/var/lib/postgresql stop'."
