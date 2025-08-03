# Cole todo o bloco acima
chmod +x ~/CompassAIPlatform/launch_compass_fullstack.sh#!/bin/bash

echo "🔧 Inicializando Plataforma CompassAI em modo contínuo (DEV + PROD Turbo)..."

# Variáveis
BACKEND_DIR=~/CompassAIPlatform/backend
FRONTEND_DIR=~/CompassAIPlatform/frontend

# Função de desenvolvimento com tmux ou fallback
start_dev() {
    echo "🧪 Modo Desenvolvimento Ativado..."

    if command -v tmux &> /dev/null; then
        echo "🧵 Usando tmux para sessões paralelas..."
        tmux new-session -d -s compass_ai
        tmux send-keys -t compass_ai "cd $BACKEND_DIR && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000" C-m
        tmux split-window -h
        tmux send-keys -t compass_ai "cd $FRONTEND_DIR && yarn install && yarn dev" C-m
        tmux attach -t compass_ai
    else
        echo "🔁 Sem tmux, executando processos paralelos..."
        (cd $BACKEND_DIR && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000) &
        (cd $FRONTEND_DIR && yarn install && yarn dev) &
        wait
    fi
}

# Função de produção com PM2
start_prod() {
    echo "🏭 Modo Produção Ativado..."

    cd $BACKEND_DIR
    source venv/bin/activate
    pm2 delete compass-backend &>/dev/null
    pm2 start uvicorn --name "compass-backend" -- "main:app" --host 0.0.0.0 --port 8000

    cd $FRONTEND_DIR
    yarn install
    yarn build
    pm2 delete compass-frontend &>/dev/null
    pm2 serve build 3000 --name "compass-frontend" --spa
}

# Execução direta das duas funções em paralelo (modo contínuo)
start_dev & start_prod & wait

echo "✅ CompassAIPlatform está rodando com backend + frontend fullstack ativados!"
