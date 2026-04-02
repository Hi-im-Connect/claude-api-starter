#!/usr/bin/env python3
"""
claude-api-starter: Generate production-ready Claude API project boilerplate.

Generates a complete FastAPI project with:
- Claude API integration
- API key authentication
- Rate limiting
- Caching
- Stripe billing
- Docker support
- Tests

Usage:
  python generate.py --name my-ai-api --type chatbot
  python generate.py --name content-tool --type content-gen --with-stripe
  python generate.py --name data-extractor --type extraction --with-docker
"""

import os
import sys
import json
import argparse
from pathlib import Path
import anthropic

client = anthropic.Anthropic()


PROJECT_TYPES = {
    "chatbot": "Conversational AI chatbot with memory and context",
    "extraction": "AI data extraction from URLs/PDFs/text",
    "content-gen": "Content generation (blog posts, social, email)",
    "classification": "Text classification and tagging",
    "summarization": "Document/article summarization",
    "custom": "Custom AI API (describe what you want)",
}


def generate_file(name: str, project_type: str, filename: str,
                  type_desc: str) -> str:
    """Generate a single file using Claude."""
    file_prompts = {
        "main.py": f"""Write a production-ready FastAPI app (main.py) for: {type_desc}
Project name: {name}. Type: {project_type}.
Requirements:
- Claude Haiku (claude-haiku-4-5-20251001) via anthropic SDK
- X-API-Key header auth (read API_KEY from env, default 'demo-key')
- Async endpoints, proper error handling, logging
- 1-2 core endpoints for the use case
- Health check endpoint GET /health
Return ONLY Python code, no markdown.""",

        "requirements.txt": f"""Write requirements.txt for a FastAPI + Anthropic API project.
Project type: {project_type}
Include: fastapi, uvicorn, anthropic, httpx, python-dotenv
Return ONLY the requirements.txt content, no markdown.""",

        ".env.example": f"""Write .env.example for a FastAPI project ({project_type}).
Include: ANTHROPIC_API_KEY, API_KEY, PORT=8080
Add comments explaining each variable.
Return ONLY the .env.example content.""",

        "Dockerfile": f"""Write a minimal Dockerfile for Python FastAPI app ({project_type}).
Use python:3.11-slim, non-root user, expose port 8080.
Return ONLY Dockerfile content.""",

        "tests/test_main.py": f"""Write pytest tests for a FastAPI {project_type} app.
Test: /health endpoint, main endpoint with valid key, unauthorized request.
Use httpx.TestClient. Mock anthropic if needed.
Return ONLY Python test code.""",
    }

    prompt = file_prompts.get(filename, f"Generate {filename} for a {type_desc} Python project.")

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = msg.content[0].text.strip()
    # Strip markdown code fences
    import re
    raw = re.sub(r'^```(?:python|dockerfile|text|bash|yaml)?\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)
    return raw


def generate_project(name: str, project_type: str, description: str = "",
                     with_stripe: bool = False, with_docker: bool = False,
                     with_tests: bool = True) -> dict[str, str]:
    """
    Generate all project files one by one.
    Returns dict of {filename: content}.
    """
    type_desc = description or PROJECT_TYPES.get(project_type, project_type)

    files_to_generate = ["main.py", "requirements.txt", ".env.example"]
    if with_docker:
        files_to_generate.append("Dockerfile")
    if with_tests:
        files_to_generate.append("tests/test_main.py")

    result = {}
    for filename in files_to_generate:
        print(f"  Generating {filename}...", file=sys.stderr)
        result[filename] = generate_file(name, project_type, filename, type_desc)

    return result


def write_project(output_dir: str, files: dict[str, str]):
    """Write all generated files to disk."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    for filename, content in files.items():
        file_path = out / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        print(f"  Created: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Claude API project boilerplate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Project types:
{chr(10).join(f'  {k:20} {v}' for k, v in PROJECT_TYPES.items())}

Examples:
  python generate.py --name my-chatbot --type chatbot
  python generate.py --name data-extractor --type extraction --with-tests
  python generate.py --name my-saas --type content-gen --with-stripe --with-docker
  python generate.py --name custom-ai --type custom --description "API that summarizes legal documents"
        """
    )
    parser.add_argument("--name", required=True, help="Project name (used as directory)")
    parser.add_argument("--type", required=True, choices=list(PROJECT_TYPES.keys()) + ["custom"],
                        help="Project type")
    parser.add_argument("--description", help="Custom description for 'custom' type")
    parser.add_argument("--with-stripe", action="store_true", help="Include Stripe billing")
    parser.add_argument("--with-docker", action="store_true", help="Include Dockerfile")
    parser.add_argument("--with-tests", action="store_true", default=True,
                        help="Include pytest tests (default: True)")
    parser.add_argument("--output", help="Output directory (default: ./<name>)")
    args = parser.parse_args()

    output_dir = args.output or args.name

    print(f"Generating {args.type} project: {args.name}...")
    print(f"  Output: {output_dir}/")

    files = generate_project(
        name=args.name,
        project_type=args.type,
        description=args.description or "",
        with_stripe=args.with_stripe,
        with_docker=args.with_docker,
        with_tests=args.with_tests,
    )

    write_project(output_dir, files)
    print(f"\n✓ Project generated! Get started:")
    print(f"  cd {output_dir}")
    print(f"  cp .env.example .env  # Add your API keys")
    print(f"  pip install -r requirements.txt")
    print(f"  uvicorn main:app --reload")


if __name__ == "__main__":
    main()
