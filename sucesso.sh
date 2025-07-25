#!/bin/bash

# Simula pedidos válidos
while true; do
  echo "🔁 Enviando pedido válido..."

  # Faz um pedido válido
  RESPONSE=$(curl -s -X POST http://localhost:5050/pedido \
    -H "Content-Type: application/json" \
    -d '{"nome": "Carlos", "cafe": "expresso"}')

  # Extrai o ID do pedido
  PEDIDO_ID=$(echo $RESPONSE | jq -r '.pedido_id')

  echo "✅ Pedido criado: $PEDIDO_ID"

  # Aguarda 2 segundos e consulta o status
  sleep 2

  STATUS=$(curl -s http://localhost:5050/status/$PEDIDO_ID)
  echo "📦 Status do pedido $PEDIDO_ID: $STATUS"

  sleep 5
done