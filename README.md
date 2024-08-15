# Gemini Integration with Python Microservice

This project demonstrates the integration of the Gemini AI model into a Python microservice using RabbitMQ for message queuing. It provides a scalable and efficient way to interact with the Gemini AI model through a RESTful API.

## Project Structure

- `app.py`: Flask web service that handles incoming requests and communicates with RabbitMQ
- `gemini_worker.py`: Worker script for Gemini API interaction
- `Dockerfile`: Docker configuration for the application
- `docker-compose.yaml`: Docker Compose configuration for the entire stack
- `requirements.txt`: Python dependencies

## Features

- RESTful API endpoint for generating content using Gemini AI
- Asynchronous processing using RabbitMQ
- Dockerized application for easy deployment
- Scalable architecture allowing multiple workers

## Prerequisites

- Docker and Docker Compose installed on your system
- Gemini API key from Google AI Studio

## Setup Instructions

1. Clone the repository:
 ```url
  https://github.com/CharisChakim/Gemini_Integration_with_Python_Microservicece.git
  ```

2. Set up your environment variables:
- Create a `.env` file in the root directory of the project
- Add the following content to the `.env` file:
  ```
  GEMINI_API_KEY=your_actual_api_key_here
  ```
- Replace `your_actual_api_key_here` with your Gemini API key

3. Update the `docker-compose.yaml` file:
- Replace the `environment` section for both `web` and `worker` services with:
  ```yaml
  environment:
    - GEMINI_API_KEY=${GEMINI_API_KEY}
  ```

4. Build and run the Docker containers:
```bash
docker-compose up --build -d
```
5. The service will be available at `http://localhost:5000`

## Usage

1. Access the home page at `http://localhost:5000` for a welcome message and usage instructions.

2. To generate content, send a POST request to `/generate` with a JSON payload containing the prompt:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt":"Kapan Indonesia Merdeka?"}' http://localhost:5000/generate
```
## Architecture Overview

This project uses a microservices architecture:

1. **Web Service (Flask)**: Handles incoming HTTP requests and publishes them to RabbitMQ.
2. **RabbitMQ**: Acts as a message broker, decoupling the web service from the Gemini API calls.
3. **Worker**: Consumes messages from RabbitMQ, sends them to the Gemini API, and publishes the responses back to RabbitMQ.

## Performance Evaluation

The current implementation provides a good balance between responsiveness and scalability. Some key points:

- Asynchronous processing allows the web service to handle multiple requests concurrently.
- RabbitMQ enables easy scaling of worker processes to handle increased load.
- The retry mechanism in the RabbitMQ connection ensures resilience against temporary network issues.

For production use, consider implementing:
- Load balancing for the web service
- Monitoring and logging solutions
- Caching frequently requested responses

## Implementation Challenges and Solutions

1. **RabbitMQ Connection Issues**: 
- Challenge: Initial connection failures when the RabbitMQ service wasn't fully ready, leading to errors during startup.
- Solution: Initially tried implementing a retry mechanism with exponential backoff, but this caused errors. Instead, simplified the connection logic by removing the retry mechanism and relying on Docker Compose's depends_on with condition: service_healthy to ensure that RabbitMQ is fully up before other services attempt to connect.

2. **Dependency Conflicts**: 
- Challenge: Version conflicts between Flask and Werkzeug.
- Solution: Not use the specific version in the requirements.txt file, so it will take the newest version.

3. **Docker Networking**: 
- Challenge: Ensuring proper communication between containerized services.
- Solution: Used Docker Compose to define the network and service dependencies.

## Acknowledgments

- Google for providing the Gemini AI API
- The Flask and RabbitMQ communities for their excellent documentation