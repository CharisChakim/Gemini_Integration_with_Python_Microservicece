from flask import Flask, request, jsonify, render_template_string
from retry import retry
import time
import pika
import json
import uuid

app = Flask(__name__)

@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def get_rabbitmq_connection():
    return pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))

connection = None
channel = None

def ensure_connection():
    global connection, channel
    if connection is None or connection.is_closed:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.queue_declare(queue='gemini_requests')
        channel.queue_declare(queue='gemini_responses')

# @app.route('/')
# def home():
#     return "Welcome to the Gemini API integration service!"

@app.route('/')
def home():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gemini API Integration Service</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }
            .container {
                text-align: center;
                background-color: white;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #4a4a4a;
            }
            p {
                color: #666;
                margin-bottom: 1rem;
            }
            code {
                background-color: #f4f4f4;
                padding: 0.2rem 0.4rem;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the Gemini API Integration Service!</h1>
            <p>This service integrates Gemini AI with a Python microservice using RabbitMQ.</p>
            <p>To use the API, send a POST request to <code>/generate</code> with a JSON payload:</p>
            <code>
                {
                    "prompt": "Your prompt here"
                }
            </code>
            <p>Example using curl:</p>
            <code>
                curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Kapan Indonesia Merdeka?"}' http://localhost:5000/generate
            </code>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/generate', methods=['POST'])
def generate():
    ensure_connection()
    
    prompt = request.json['prompt']
    correlation_id = str(uuid.uuid4())

# Publish
    channel.basic_publish(
        exchange='',
        routing_key='gemini_requests',
        properties=pika.BasicProperties(
            reply_to='gemini_responses',
            correlation_id=correlation_id,
        ),
        body=json.dumps({'prompt': prompt})
    )

########## if error in 30 seconds
    for _ in range(30):  
        method_frame, properties, body = channel.basic_get(queue='gemini_responses')
        if properties and properties.correlation_id == correlation_id:
            response = json.loads(body)
            return jsonify(response)
        time.sleep(1)

    return jsonify({"error": "Timeout waiting for response"}), 408

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)