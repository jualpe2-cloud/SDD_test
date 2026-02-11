# Contributing to SDD_test

Thank you for your interest in contributing! This document provides guidelines for contributing to the Strava Routes Export API project.

## Project Structure

```
SDD_test/
├── FUNCTIONAL_REQUIREMENTS.md    # Feature requirements
├── STRAVA_INTEGRATION.md         # Integration guide
├── openapi.yaml                  # API specification
├── specs/                        # Detailed specifications
├── app/                          # FastAPI application
│   ├── main.py                   # Entry point
│   ├── config.py                 # Configuration
│   ├── routes/                   # Route handlers
│   ├── services/                 # Business logic
│   ├── models/                   # Data models
│   └── utils/                    # Utility functions
├── tests/                        # Test suite
├── requirements.txt              # Python dependencies
└── docker-compose.yml            # Development environment
```

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/jualpe2-cloud/SDD_test.git
cd SDD_test

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your Strava credentials
```

### 2. Running the Application

```bash
# Development server
uvicorn app.main:app --reload --port 8000

# With Docker
docker-compose up
```

### 3. Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_routes.py

# Run with coverage
pytest --cov=app tests/
```

## Feature Implementation Guidelines

### Before Starting
1. Read the specification in specs/FR*.md
2. Review the linked GitHub Issue
3. Check the OpenAPI spec in openapi.yaml

### During Development
1. Follow the specification exactly
2. Write tests first (TDD approach)
3. Keep functions small and focused
4. Add docstrings to all functions
5. Handle errors gracefully

### Code Standards
- Use type hints
- Follow PEP 8
- Keep functions under 50 lines
- Use descriptive variable names
- Comment complex logic

## Making a Pull Request

1. Create a feature branch: git checkout -b feature/FR-1.1
2. Commit changes: git commit -m "Implement FR1.1: List routes"
3. Push branch: git push origin feature/FR-1.1
4. Open PR with reference to GitHub Issue

## Testing Requirements

- All new code must have tests
- Tests should cover success and error scenarios
- Use pytest for unit tests
- Mock external API calls (Strava)
- Aim for 80%+ code coverage

## Documentation

- Update README.md if adding new features
- Add docstrings to all functions
- Include examples in docstrings
- Update FUNCTIONAL_REQUIREMENTS.md if scope changes

## Questions?

- Check existing issues and PRs
- Review specification documents
- Ask in GitHub Discussions

Thank you for contributing!