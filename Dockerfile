# Use a imagem oficial do Python como base
FROM python:3.12.1

# Define a variável de ambiente para não gerar .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Define a variável de ambiente para não armazenar cache do Python
ENV PYTHONUNBUFFERED 1

# Cria e define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt ./
COPY wait-for-db.sh ./

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copia o código fonte da aplicação para o contêiner
COPY . .

# Executa o comando collectstatic
RUN python manage.py collectstatic --noinput

# Inicia o Gunicorn
CMD ["sh", "-c", "./wait-for-db.sh && python manage.py migrate && gunicorn --log-level debug --error-logfile - --access-logfile - setup.wsgi:application --bind 0.0.0.0:8000"]



