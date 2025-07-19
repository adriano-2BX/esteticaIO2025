# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python. Certifique-se de instalar as dependências de MySQL
# antes de qualquer outra coisa, para evitar problemas de compilação.
# A dependência mysqlclient precisa de algumas bibliotecas de desenvolvimento no sistema operacional.
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# --host 0.0.0.0 é crucial para que o container possa ser acessado externamente
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
