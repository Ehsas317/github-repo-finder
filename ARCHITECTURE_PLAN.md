# Architecture Plan: GitHub Repo Finder

## 1. Directory Structure
```text
github-repo-finder/
├── .github/
│   └── workflows/
│       ├── ci.yml          # Tests, Linting, Type-checking
│       └── release.yml     # Automated releases
├── configs/
│   └── default_config.yaml # Default scoring weights and API settings
├── docs/
│   ├── architecture.md
│   ├── developer_guide.md
│   ├── troubleshooting.md
│   └── api_reference.md
├── examples/
│   ├── basic_search.py
│   ├── mcp_usage.md
│   └── cli_examples.sh
├── prompts/
│   └── llm_formatting.txt  # System prompts for LLM output modes
├── schemas/
│   ├── repo_schema.json    # JSON schema for repository data
│   └── config_schema.json  # JSON schema for configuration
├── src/
│   └── github_repo_finder/
│       ├── __init__.py
│       ├── cli.py          # CLI Entry point
│       ├── mcp.py          # MCP Server implementation
│       ├── core/
│       │   ├── __init__.py
│       │   ├── search.py    # GitHub API client wrapper
│       │   ├── ranking.py   # Scoring and ranking logic
│       │   ├── models.py    # Data classes (Repository, SearchResult)
│       │   └── engine.py    # Orchestrator
│       └── utils/
│           ├── __init__.py
│           ├── caching.py   # SQLite or File-based cache
│           ├── token_opt.py # Token counting and optimization
│           ├── errors.py    # Custom exceptions
│           └── formatters.py # Markdown/JSON/Compact/LLM formatters
├── tests/
│   ├── __init__.py
│   ├── test_search.py
│   ├── test_ranking.py
│   ├── test_caching.py
│   └── test_cli.py
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml         # Build system and dependencies
├── README.md
└── SKILL.md               # Claude/ChatGPT skill definition
```

## 2. Core Components Detail

### A. Search Engine (`core/search.py`)
- Uses `requests` or `httpx` for GitHub REST API.
- Implements retry logic with exponential backoff.
- Handles rate limiting gracefully.
- Supports advanced filters (stars, date, language, license).

### B. Ranking Engine (`core/ranking.py`)
- Implements the scoring logic from `pasted_content_2.txt`.
- **Weights:** Stars (40%), Recency (30%), Forks (15%), Activity Health (15%).
- Provides a "Maintenance Score" and "Freshness Score".

### C. Token Optimizer (`utils/token_opt.py`)
- Estimates token usage for different output formats.
- Implements "Compact" mode: stripping unnecessary fields like `node_id`, `blobs_url`, etc.
- Deduplication: ensuring the same repo isn't returned twice in a session.

### D. Caching (`utils/caching.py`)
- Persistent cache for API responses to save tokens and money.
- TTL-based expiration.

### E. MCP Server (`mcp.py`)
- Implements the Model Context Protocol.
- Exposes tools: `search_repos`, `get_trending`, `get_repo_details`.

### F. CLI (`cli.py`)
- Rich CLI using `typer` or `click`.
- Beautiful output using `rich`.

## 3. Implementation Phases
1. **Core Library**: Models, Search, Ranking, Caching.
2. **Interfaces**: CLI, MCP, API.
3. **Quality**: Tests, CI/CD, Linting.
4. **Documentation**: Full suite of docs.
5. **Review**: Security and Performance audit.
