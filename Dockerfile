# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho onde o pacote 'app' ficará
# O EasyPanel vai copiar o contexto do seu repositório para este diretório.
WORKDIR /usr/src/app

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python usando pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do seu repositório (incluindo a pasta 'app') para o WORKDIR
COPY . .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# Agora, 'app.main:app' funciona porque 'app' é uma pasta (um pacote Python)
# dentro do diretório de trabalho '/usr/src/app'.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
