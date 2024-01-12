#!/bin/bash

# Aguarde o banco de dados ficar pronto
while ! timeout 1 bash -c 'cat < /dev/null > /dev/tcp/db/3306'; do
  echo "Waiting for MySQL..."
  sleep 1
done

exec "$@"