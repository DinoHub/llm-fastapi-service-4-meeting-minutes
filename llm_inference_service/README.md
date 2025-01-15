# LLM Inference Service

A Python-based service for deploying large language models (LLMs) using NVIDIA CUDA for accelerated inference. This repository provides a containerized solution built with a multi-stage Dockerfile, leveraging Poetry for dependency management.

## Features

- **CUDA Support**: Optimized for NVIDIA GPUs with CUDA 12.1.
- **Python 3.12**: Fully compatible with the latest Python version.
- **Poetry Integration**: Simplified dependency management and virtual environment bundling.
- **Secure Runtime**: Runs as a non-root user in the container.
- **REST API**: Uses `vllm.entrypoints.openai.api_server` for OpenAI-compatible API endpoints.

## Getting Started

### Prerequisites
Before getting started, ensure you have the following installed:

- NVIDIA Drivers: Ensure your system has the appropriate NVIDIA drivers installed.
- Docker: Install Docker CE (version 20.10+).
- NVIDIA Container Toolkit (for GPU support): Configure Docker to use NVIDIA GPUs.

Additionally, confirm you have a compatible GPU and CUDA setup.

### Building the Docker Image
Clone this repository and navigate to the directory containing the `Dockerfile`:

```bash
git clone <repo-url>
cd <repo-folder>
```
Build the Docker image using the following command:

```bash
docker build -t llm-inference-service .
```

### Usage

Run the container:

```bash
docker run --gpus all -p 8000:8000 llm-inference-service
```

This will start the REST API server. By default, it listens on port 8000.

### Example API Request

Send a request to the inference API:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
           "model": "meta-llama/Meta-Llama-3-8B",
           "messages": [{"role": "user", "content": "why is the sky blue?"}],
         }'
```

## Acknowledgments

- Built on top of the amazing [vLLM](https://github.com/vllm-project/vllm).
- Thanks to the open-source community for providing tools like Poetry and CUDA.
