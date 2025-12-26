# Helix - Triple Helix Innovation Chatbot

A specialized chatbot service for discussing innovation systems through the lens of the Triple Helix model.

## What is Triple Helix?

The **Triple Helix** is an influential innovation model that describes the dynamic interaction between three key institutional spheres:

1. **🎓 University** (Academia/Research)
   - Knowledge creation and fundamental research
   - Education and human capital development
   - Scientific publications and patents

2. **🏭 Industry** (Business/Private Sector)
   - Technology development and commercialization
   - Product innovation and market application
   - Economic growth and job creation

3. **🏛️ Government** (Public Sector/Policy)
   - Regulatory frameworks and policies
   - Funding and infrastructure support
   - Strategic direction and coordination

The Triple Helix model emphasizes how these three sectors collaborate, overlap, and exchange roles to drive innovation and economic development. It recognizes that innovation increasingly occurs at the interfaces between these spheres, leading to:

- **Knowledge transfer** between universities and industry
- **Technology transfer** and commercialization
- **Public-private partnerships**
- **Regional innovation ecosystems**
- **Science parks and incubators**

This framework helps understand modern innovation systems and develop strategies for fostering innovation-driven economic growth.

## About This Project

This project provides a chatbot service that answers questions about innovation, technology transfer, and economic development through the Triple Helix perspective. The chatbot:

- ✅ Provides evidence-based answers consistent with Triple Helix research
- ✅ Includes citations to academic papers, reports, and credible sources
- ✅ Can incorporate custom PDF documents for context
- ✅ Logs conversation transcripts for analysis
- ✅ Available as both CLI tool and REST API service

## Features

### Two Deployment Modes

1. **CLI Tool** (`triple-helix-innovation.py`)
   - Interactive command-line chatbot
   - Supports loading up to 2 PDF documents for context
   - Saves timestamped conversation transcripts
   - Simple text-based interface

2. **REST API Service** (`helix/api.py`)
   - FastAPI-based HTTP service
   - Multi-turn conversation support
   - Custom context documents
   - Health check and readiness endpoints
   - Production-ready with logging and monitoring

## Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API key (required for live responses)

### Installation

```bash
# Clone the repository
git clone https://github.com/yabo1234/helix.git
cd helix

# Install dependencies
pip install -r requirements.txt

# For PDF support in CLI (optional)
pip install pypdf
```

### Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

Optional environment variables:

```bash
# For CLI tool
export HELIX_MODEL='gpt-5.2'  # Default model

# For API service
export OPENAI_BASE_URL='https://api.openai.com/v1'  # OpenAI base URL
export HELIX_ACCESS_MODE='public'  # or 'private' for API key auth
export HELIX_API_KEY='your-service-api-key'  # Required if access_mode=private
export HELIX_DRY_RUN='false'  # Set to 'true' to test without OpenAI calls (CLI + API)
export LOG_FORMAT='json'  # or 'text'
export LOG_LEVEL='INFO'  # DEBUG, INFO, WARNING, ERROR
```

## Usage

### CLI Tool

Run the interactive chatbot:

```bash
python triple-helix-innovation.py
```

To run without making OpenAI calls (no API key required):

```bash
HELIX_DRY_RUN=true python triple-helix-innovation.py
```

You'll be prompted to:
1. Optionally provide a directory containing PDF documents for context
2. Enter your questions and receive answers
3. Type `exit` or `quit` to end the session

Transcripts are saved to `./transcripts/triple_helix_chat_YYYYMMDD_HHMMSS_UTC.txt`

### API Service

#### Local Development

Start the API server:

```bash
uvicorn helix.api:app --reload --port 8080
```

#### API Endpoints

**Health Check**
```bash
curl http://localhost:8080/healthz
```

**Readiness Check**
```bash
curl http://localhost:8080/readyz
```

**Chat Endpoint**

```bash
curl -X POST http://localhost:8080/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the key principles of the Triple Helix model?",
    "messages": [],
    "context_documents": [],
    "temperature": 0.2
  }'
```

For private mode (requires API key):
```bash
curl -X POST http://localhost:8080/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"message": "Your question here"}'
```

#### Request Schema

```json
{
  "message": "Your question",
  "messages": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ],
  "context_documents": ["Additional context text"],
  "system_prompt": "Optional custom system prompt",
  "model": "gpt-5.2",
  "temperature": 0.2,
  "max_output_tokens": 4096,
  "metadata": {}
}
```

#### Response Schema

```json
{
  "id": "unique-response-id",
  "created_at": "2025-12-20T01:00:00Z",
  "model": "gpt-5.2",
  "response": "The chatbot's answer with citations",
  "openai_response_id": "openai-request-id",
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 200,
    "total_tokens": 300
  }
}
```

## Docker Deployment

Build the Docker image:

```bash
docker build -t helix:latest .
```

Run the container:

```bash
docker run -p 8080:8080 \
  -e OPENAI_API_KEY='your-key' \
  -e HELIX_MODEL='gpt-5.2' \
  helix:latest
```

## Google Cloud Run Deployment

1. Edit `cloudrun.service.yaml` with your project details
2. Build and push the image:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/helix:latest
```

3. Deploy to Cloud Run:

```bash
gcloud run services replace cloudrun.service.yaml
```

## System Prompt

The chatbot uses a specialized system prompt that:
- Ensures all answers align with Triple Helix innovation research
- Requires citations for factual claims (e.g., [Author, Year])
- Requests evidence-based, specific, and actionable responses
- Acknowledges uncertainty when claims aren't well-supported

## Project Structure

```
helix/
├── helix/                          # API service package
│   ├── __init__.py
│   ├── api.py                      # FastAPI application
│   ├── auth.py                     # API key authentication
│   ├── config.py                   # Configuration management
│   ├── logging_config.py           # Logging setup
│   ├── openai_client.py            # OpenAI API client
│   ├── prompts.py                  # System prompts
│   └── request_context.py          # Request context handling
├── triple-helix-innovation.py      # CLI chatbot
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker build configuration
├── cloudrun.service.yaml           # Cloud Run deployment config
└── README.md                       # This file
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests (when available)
pytest
```

### Code Quality

```bash
# Format code
black .

# Type checking
mypy helix/

# Linting
ruff check .
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Submit a pull request

## License

This project is provided as-is for educational and research purposes.

## References

Key publications on the Triple Helix model:

- Etzkowitz, H., & Leydesdorff, L. (2000). The dynamics of innovation: from National Systems and "Mode 2" to a Triple Helix of university–industry–government relations. *Research Policy*, 29(2), 109-123.
- Leydesdorff, L., & Etzkowitz, H. (1998). The Triple Helix as a model for innovation studies. *Science and Public Policy*, 25(3), 195-203.
- Etzkowitz, H. (2008). *The Triple Helix: University-Industry-Government Innovation in Action*. Routledge.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Review conversation transcripts for debugging
- Check logs for detailed error messages

---

**Note**: This chatbot provides information based on academic research and should not be considered as professional consulting advice. Always verify important decisions with domain experts.
