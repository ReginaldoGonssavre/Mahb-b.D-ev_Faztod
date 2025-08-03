# Imagem base Python + Node.js
FROM python:3.11-slim

# Instala Node.js (exemplo: Node 18)
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instala dependências Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Instala dependências Node.js (frontend)
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm install --production

# Copia o restante do código backend e frontend
COPY . .

# Compila o frontend React
RUN cd frontend && npm run build

# Coleta arquivos estáticos do Django
RUN python manage.py collectstatic --noinput

EXPOSE 8000 3000

# Inicialização paralela do backend (Django) e do frontend (React com serve)
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000 & npx serve -s frontend/build -l 3000