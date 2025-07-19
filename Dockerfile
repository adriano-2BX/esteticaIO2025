# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
# É importante copiar requirements.txt antes do resto do código para que o cache do Docker funcione bem
COPY requirements.txt .

# Instala as dependências Python.
# A dependência mysqlclient precisa de algumas bibliotecas de desenvolvimento no sistema operacional.
# Instalamos elas, rodamos o pip install, e depois as removemos para manter a imagem pequena.
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o restante do código da aplicação (todo o conteúdo de ./app/ para /app no container)
COPY ./app .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# A aplicação principal agora está em 'app.main:app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
