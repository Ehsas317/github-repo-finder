# Developer Guide

This guide provides information for developers who want to contribute to or extend the `github-repo-finder` project.

## Project Structure

```
github-repo-finder/
├── .github/              # GitHub Actions workflows
├── configs/              # Configuration files
├── docs/                 # Project documentation
├── examples/             # Usage examples
├── prompts/              # LLM prompt templates
├── schemas/              # JSON schemas for data validation
├── src/
│   └── github_repo_finder/
│       ├── __init__.py
│       ├── cli.py        # Command-Line Interface
│       ├── mcp.py        # Model Context Protocol server
│       └── core/         # Core logic
│           ├── __init__.py
│           ├── search.py # GitHub API client
│           ├── ranking.py# Repository ranking logic
│           ├── models.py # Data models
│           └── engine.py # Orchestrator
│       └── utils/        # Utility functions
│           ├── __init__.py
│           ├── caching.py# Caching mechanism
│           ├── token_opt.py# Token optimization
│           ├── errors.py # Custom exceptions
│           └── formatters.py # Output formatters (planned)
├── tests/                # Unit and integration tests
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml        # Project metadata and dependencies
├── README.md
└── SKILL.md              # LLM skill definition
```

## Setting up Development Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ehsas317/github-repo-finder.git
    cd github-repo-finder
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -e .[dev]
    ```
    This will install the project in editable mode and include development dependencies like `pytest`, `black`, and `isort`.

3.  **GitHub Token:**
    For making authenticated requests to the GitHub API and avoiding strict rate limits, it's highly recommended to set a GitHub Personal Access Token (PAT).
    You can generate one [here](https://github.com/settings/tokens) with `public_repo` scope.
    Set it as an environment variable:
    ```bash
    export GITHUB_TOKEN="YOUR_GITHUB_PAT"
    ```
    Or pass it directly to the CLI using `--token` argument.

## Running Tests

To run the test suite:

```bash
pytest tests/
```

To run tests with coverage report:

```bash
pytest --cov=github_repo_finder tests/
```

## Code Style and Formatting

We use `black` for code formatting and `isort` for sorting imports. Please run these tools before committing your changes:

```bash
black .
isort .
```

## Adding New Features

When adding new features, consider the following:

-   **Modularity**: Keep components loosely coupled and focused on a single responsibility.
-   **Testability**: Write unit and integration tests for all new functionality.
-   **Token Optimization**: Always consider the impact on token usage, especially for LLM-facing outputs.
-   **Error Handling**: Implement robust error handling and provide meaningful error messages.
-   **Documentation**: Update relevant documentation (README, developer guide, API reference) for any new features or changes.

## Extending the Ranking Engine

The `RankingEngine` in `src/github_repo_finder/core/ranking.py` is designed to be extensible. You can modify the weights or add new scoring criteria by adjusting the `calculate_score` method and its helpers.

## Caching

The `CacheManager` in `src/github_repo_finder/utils/caching.py` uses SQLite. If you need a different caching mechanism (e.g., Redis), you can implement a new caching class that adheres to the same `get`, `set`, `delete`, and `clear` interface.

## MCP Server

The `MCPServer` in `src/github_repo_finder/mcp.py` defines the tools exposed to LLMs. To add a new tool, you need to:

1.  Define the tool's schema in the `get_tools` method.
2.  Implement the logic for the tool in the `call_tool` method.

## Contribution Workflow

Please refer to `CONTRIBUTING.md` for the detailed contribution workflow, including branching strategy and pull request guidelines.
