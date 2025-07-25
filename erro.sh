#!/bin/bash

# Simula requisições inválidas
while true; do
  echo "❌ Enviando pedido inválido..."

  curl -s -X POST http://localhost:5050/pedido \
    -H "Content-Type: application/json" \
    -d '{"nome": "Erro", "cafe": "mocha"}' | jq

  sleep 4
done
