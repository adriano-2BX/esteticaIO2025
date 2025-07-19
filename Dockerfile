# Use uma imagem oficial do Python como base (versão completa do Debian Buster)
FROM python:3.9-buster

# Define o diretório de trabalho dentro do container
WORKDIR /usr/src/app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python usando pip
# Como a imagem 'buster' já tem muitas ferramentas de build, esta etapa deve ser suficiente.
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do seu repositório (incluindo a pasta 'app') para o WORKDIR
COPY . .

# Explicitamente adiciona o diretório de trabalho ao PYTHONPATH
# Isso garante que o Python encontre o pacote 'app'
ENV PYTHONPATH=/usr/src/app

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
