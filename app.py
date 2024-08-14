from flask import Flask, request, jsonify
import pika
import json
import uuid
from retry import retry
import time

app = Flask(__name__)

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

# Initialize connection as None
connection = None
channel = None

def ensure_connection():
    global connection, channel
    if connection is None or connection.is_closed:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue='gemini_requests')
        channel.queue_declare(queue='gemini_responses')

@app.route('/')
def home():
    return "Welcome to the Gemini API integration service!"

@app.route('/generate', methods=['POST'])
def generate():
    ensure_connection()
    
    prompt = request.json['prompt']
    correlation_id = str(uuid.uuid4())

    # Publish request to RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='gemini_requests',
        properties=pika.BasicProperties(
            reply_to='gemini_responses',
            correlation_id=correlation_id,
        ),
        body=json.dumps({'prompt': prompt})
    )

    # Wait for the response
    for _ in range(30):  # Try for 30 seconds
        method_frame, properties, body = channel.basic_get(queue='gemini_responses')
        if properties and properties.correlation_id == correlation_id:
            response = json.loads(body)
            return jsonify(response)
        time.sleep(1)

    return jsonify({"error": "Timeout waiting for response"}), 408

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)