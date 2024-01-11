#!/bin/bash
echo "v2 sem netcat"
# Aguarde o banco de dados ficar pronto
while ! timeout 1 bash -c 'cat < /dev/null > /dev/tcp/db/3306'; do
  echo "Waiting for MySQL..."
  sleep 1
done

# Execute as migrations
echo "Running migrations..."
python manage.py migrate

# Inicie o servidor web
echo "Starting server..."
exec "$@"