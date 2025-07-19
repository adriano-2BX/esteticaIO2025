# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do sistema operacional necessárias para bcrypt e cryptography
# E então, instala as dependências Python.
RUN apt-get update --fix-missing -y \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    # Limpa o cache do apt imediatamente após a instalação para reduzir o tamanho da imagem final
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential libffi-dev \
    && apt-get autoremove -y \
    && apt-get clean

# Copia todo o conteúdo do seu repositório (incluindo a pasta 'app') para o WORKDIR
COPY . .

# Explicitamente adiciona o diretório de trabalho ao PYTHONPATH
ENV PYTHONPATH=/usr/src/app

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
