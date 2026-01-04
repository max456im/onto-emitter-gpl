#!/bin/bash
# GPL-3.0-only — запрещено подключать сторонние данные

set -e

echo "[*] Проверка лицензии..."
if [ ! -f "../../LICENSE" ]; then
  echo "[!] LICENSE не найден. Остановка."
  exit 1
fi

echo "[*] Сборка Docker-образа..."
docker build -f ../docker/Dockerfile -t onto-emitter-gpl:$(date +%Y%m%d) ../../

echo "[*] Образ готов. Лицензионная изоляция соблюдена."