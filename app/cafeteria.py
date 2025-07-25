from flask import Flask, request, jsonify
from ddtrace import patch_all, tracer
from werkzeug.exceptions import BadRequest, NotFound
import random
import logging
import os

patch_all()

# Caminho absoluto do arquivo de log
LOG_PATH = os.path.abspath("cafeteria.log")

# Custom formatter para incluir trace_id e span_id nos logs
class DatadogLogFormatter(logging.Formatter):
    def format(self, record):
        span = tracer.current_span()
        if span:
            record.dd_trace_id = span.trace_id
            record.dd_span_id = span.span_id
        else:
            record.dd_trace_id = 0
            record.dd_span_id = 0
        return super().format(record)

# Criação do handler com formatter personalizado
formatter = DatadogLogFormatter(
    "%(asctime)s [%(levelname)s] trace_id=%(dd_trace_id)s span_id=%(dd_span_id)s %(message)s"
)

handler = logging.FileHandler(LOG_PATH)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

# Aplicação Flask
app = Flask(__name__)

pedidos = {}
cafes_disponiveis = ["expresso", "latte", "capuccino"]

@app.route("/")
def inicio():
    logger.info("Acesso à página inicial.")
    return "☕ Bem-vindo à Cafeteria Digital!"

@app.route("/pedido", methods=["POST"])
def fazer_pedido():
    dados = request.json
    nome = dados.get("nome")
    cafe = dados.get("cafe")

    logger.info(f"Recebido pedido de {nome} para café: {cafe}")

    if cafe not in cafes_disponiveis:
        logger.error(f"Erro: Café '{cafe}' não disponível.")
        raise BadRequest(f"Café '{cafe}' não disponível.")

    pedido_id = str(random.randint(1000, 9999))
    pedidos[pedido_id] = {"nome": nome, "cafe": cafe, "status": "em preparo"}

    logger.info(f"Pedido criado: {pedido_id} - {nome} pediu {cafe}")
    return jsonify({"mensagem": "Pedido realizado com sucesso!", "pedido_id": pedido_id})

@app.route("/status/<pedido_id>")
def status_pedido(pedido_id):
    pedido = pedidos.get(pedido_id)
    if not pedido:
        logger.warning(f"Consulta a pedido inexistente: {pedido_id}")
        raise NotFound("Pedido não encontrado.")

    logger.info(f"Consulta ao status do pedido: {pedido_id}")
    return jsonify(pedido)

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"erro": str(e)}), 400

@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({"erro": str(e)}), 404

if __name__ == "__main__":
    logger.info("🚀 Iniciando a aplicação Cafeteria Digital...")
    app.run(host="0.0.0.0", port=5050)
