# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação (todo o conteúdo de ./app/ para /app no container)
# Agora, os arquivos como main.py e database.py estarão DIRETAMENTE em /app dentro do container.
COPY ./app .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# Como os arquivos de app/ foram copiados para a raiz do WORKDIR (/app),
# o caminho do módulo agora é simplesmente 'main:app'.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
