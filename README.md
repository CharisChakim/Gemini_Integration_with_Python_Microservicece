# System_Integration_with_Gemini

This project demonstrates the integration of the Gemini AI model into a Python microservice using RabbitMQ for message queuing.

## Project Structure

- `app.py`: Flask web service
- `gemini_worker.py`: Worker script for Gemini API interaction
- `Dockerfile`: Docker configuration for the application
- `docker-compose.yaml`: Docker Compose configuration for the entire stack
- `requirements.txt`: Python dependencies

## Setup Instructions

1. Clone the repository
2. Set up your Gemini API key:
- Obtain an API key from Google AI Studio
- Replace `YOUR_GEMINI_API_KEY` in `docker-compose.yaml`,and `gemini_worker.py` with your actual API key

3. Build and run the Docker containers:
    ```docker-compose up --build```

*Note* : Make sure all container run properly. If you find container stuck on created, start it manually via your docker desktop

4. The service will be available at `http://localhost:5000`

## Usage

Send a POST request to `/generate` with a JSON payload containing the prompt:
    ``` curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Kapan Indonesia Emas itu???"}' http://localhost:5000/generate ```

