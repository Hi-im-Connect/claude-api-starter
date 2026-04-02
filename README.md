# Claude/OpenRouter API Starter Kit

Project generator for AI-powered apps. Generates a complete project structure with streaming, function calling, conversation history, and cost tracking. Works with OpenRouter (free) or Anthropic Claude.

## Quick Start

```bash
python3 generate.py my-ai-app

# With options
python3 generate.py my-chatbot --type chatbot --provider openrouter
python3 generate.py my-analyzer --type document-analyzer --provider anthropic
python3 generate.py my-assistant --type code-assistant --framework fastapi
```

## Generated Project Includes

- `main.py` — Core AI logic with streaming support
- `config.py` — Environment-based config (API keys, model selection, cost limits)
- `tools.py` — Function calling / tool use setup
- `history.py` — Conversation history management (SQLite)
- `costs.py` — Token tracking and cost estimation
- `app.py` — FastAPI or Flask web server (optional)
- `requirements.txt` — All dependencies
- `README.md` — Project-specific documentation
- `.env.example` — Environment variable template

## Project Types

- `chatbot` — Multi-turn conversational AI
- `document-analyzer` — PDF/text analysis pipeline
- `code-assistant` — Code review and generation
- `data-extractor` — Structured data extraction from text/HTML
- `content-generator` — Blog posts, emails, social media

## Providers

- `openrouter` — Free models available, 1M+ context window
- `anthropic` — Claude Haiku/Sonnet/Opus
- `both` — Auto-fallback from OpenRouter to Anthropic

## Requirements

- Python 3.10+
- No API key needed for generation — keys go in the generated `.env`

## License

MIT
