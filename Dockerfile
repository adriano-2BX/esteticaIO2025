# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define um argumento de build para invalidar o cache do apt-get update
ARG BUILD_DATE

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do sistema operacional necessárias para mysqlclient
# e as dependências Python.
# O pacote 'libmysqlclient-dev' é o mais comum e genérico.
# O uso de BUILD_DATE força uma reavaliação desta camada do Dockerfile.
RUN apt-get update --fix-missing -y \
    && apt-get install -y \
    libmysqlclient-dev \
    build-essential \
    pkg-config \
    # Limpa o cache do apt para reduzir o tamanho da imagem final
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential pkg-config \
    && apt-get autoremove -y \
    && apt-get clean

# Copia o restante do código da aplicação (todo o conteúdo de ./app/ para /app no container)
COPY ./app .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# A aplicação principal agora está em 'app.main:app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
