# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

kcopa-chatbot is a Python-based chatbot application built with FastAPI. The project is in early development stages.

## Development Setup

This project uses **uv** as the package manager (not pip or poetry).

### Essential Commands

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py

# Run with FastAPI development server (when implemented)
uv run fastapi dev main.py

# Add a new dependency
uv add <package-name>

# Remove a dependency
uv remove <package-name>
```

## Project Structure

- `main.py` - Application entry point
- `pyproject.toml` - Project metadata and dependencies managed by uv
- `uv.lock` - Locked dependency versions (managed by uv)
- `.env` - Environment variables including HuggingFace token (HF_TOKEN)

## Key Technologies

- **Python 3.11+** - Minimum required version
- **FastAPI** - Web framework (with standard extras)
- **uv** - Fast Python package manager and project manager
- **HuggingFace** - The project uses HuggingFace (HF_TOKEN is configured in .env)
- **Langcahain** - The project uses Langchain

## Important Notes

- Always use `uv run` to execute Python commands to ensure proper virtual environment activation
- The project uses `.env` file for environment variables - ensure HF_TOKEN is set for HuggingFace API access
- This is a new project with minimal code - main.py currently contains only a basic hello world function
