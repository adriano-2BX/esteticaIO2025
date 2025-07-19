# Use uma imagem oficial do Python como base
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Adiciona um argumento de build para garantir que a linha de atualização do apt não seja cacheada.
# Isso força o Docker a executar 'apt-get update' toda vez que o BUILD_ID mudar,
# o que pode ser feito passando o timestamp atual ao chamar docker build.
# O EasyPanel pode ter uma forma de fazer isso ou você pode tentar adicionar um valor dinâmico.
ARG BUILD_ID=1

# Instala as dependências do sistema operacional necessárias para mysqlclient
# e as dependências Python.
# O pacote 'libmysqlclient-dev' é o mais comum e genérico.
# Usamos && \ para que todo o comando RUN seja uma única camada,
# o que é bom para otimização do tamanho final da imagem.
RUN apt-get update --fix-missing -y \
    && apt-get install -y --no-install-recommends \
    libmysqlclient-dev \
    build-essential \
    pkg-config \
    # Limpa o cache do apt para reduzir o tamanho da imagem final IMEDIATAMENTE após a instalação
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential pkg-config \
    && apt-get autoremove -y \
    && apt-get clean

# Copia o arquivo de requisitos para o diretório de trabalho (repetido para garantir que o cache do pip não afete)
COPY requirements.txt .

# Copia o restante do código da aplicação (todo o conteúdo de ./app/ para /app no container)
COPY ./app .

# Expõe a porta que o Uvicorn irá escutar
EXPOSE 8000

# Comando para rodar a aplicação usando Uvicorn
# A aplicação principal agora está em 'app.main:app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
