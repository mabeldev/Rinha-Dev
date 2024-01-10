# Use a imagem oficial do Python como base
FROM python:3.12.1

# Define a variável de ambiente para não gerar .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Define a variável de ambiente para não armazenar cache do Python
ENV PYTHONUNBUFFERED 1

# Cria e define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instala as dependências listadas no requirements.txt
RUN pip install -r requirements.txt

# Copia o código fonte da aplicação para o contêiner
COPY . /app/