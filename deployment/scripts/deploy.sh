#!/bin/bash
set -e

ENV_FILE="../env/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "[!] Отсутствует .env — скопируйте .env.example"
  exit 1
fi

source "$ENV_FILE"

echo "[*] Запуск через docker-compose..."
docker-compose -f ../docker/docker-compose.yml up -d

echo "[*] Развёртывание завершено. Проверьте healthcheck."