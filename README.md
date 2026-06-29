# GitHub Repo Finder

## Project Goal

This project aims to build a **production-grade GitHub Repo Finder** that can be used as a Claude Skill, ChatGPT Skill, MCP Server, Standalone CLI, Python package, and API component. The system is designed to help LLMs discover the best GitHub repositories while minimizing token usage and maximizing reliability.

## Features

The GitHub Repo Finder includes the following core features:

- **GitHub Search**: Advanced searching capabilities using GitHub's API.
- **Ranking Engine**: A sophisticated ranking algorithm to score repositories based on various metrics.
- **Deduplication**: Ensures unique repositories are returned, avoiding redundant information.
- **Token Optimization**: Strategies to minimize token usage for LLM interactions.
- **Trending Repositories**: Identification of currently trending and viral repositories.
- **Filtering**: Comprehensive filtering options by language, date, stars, and license.
- **Scoring**: Maintenance score, repository health score, activity score, popularity score, freshness score, and a final weighted ranking.

## Installation

To install the `github-repo-finder` package, you can use pip:

```bash
pip install github-repo-finder
```

For development, clone the repository and install in editable mode:

```bash
git clone Ehsas317/github-repo-finder.git
cd github-repo-finder
pip install -e .
```

## Usage (CLI)

The `github-repo-finder` can be used directly from the command line:

```bash
github-repo-finder "machine learning" --limit 5 --mode markdown
```

**Arguments:**

- `query`: The search query (e.g., 'machine learning', 'python web framework').
- `--limit`: Number of results to return (default: 10).
- `--mode`: Output format. Choices: `markdown`, `detailed`, `json`, `compact`, `llm` (default: `markdown`).
- `--token`: Your GitHub Personal Access Token (optional, but recommended to avoid rate limits).
- `--no-cache`: Disable caching for the current search.

## Output Modes

The tool supports several output modes to cater to different needs:

- **Markdown**: Human-readable Markdown format.
- **Detailed**: More verbose Markdown output with additional scoring details.
- **JSON**: Structured JSON output, ideal for programmatic consumption.
- **Compact**: A highly compressed JSON format, optimized for minimal token usage.
- **LLM**: A token-optimized JSON format specifically designed for LLM consumption.

## Token Optimization

Token optimization is a critical aspect of this project. The system employs several strategies:

- **Caching**: Results are cached to avoid repeated API calls and token usage.
- **Deduplication**: Prevents duplicate repositories from being processed or returned.
- **Concise Prompts**: Designed to keep LLM prompts as short as possible.
- **Minimal Metadata**: Only essential data is returned, especially in `compact` and `llm` modes.

## Error Handling

The system is built with robust error handling to ensure reliability:

- **GitHub Rate Limits**: Implements retry logic with exponential backoff.
- **Network Failures**: Graceful handling of network issues.
- **Invalid Queries**: Provides informative error messages for malformed inputs.
- **Missing/Archived Repositories**: Filters out or handles repositories that are no longer available or relevant.
- **Partial Failures**: Designed to continue operating even if some data sources fail.

## Testing

Comprehensive tests are included to ensure the reliability and correctness of the system. This includes unit tests for individual components and integration tests for end-to-end flows.

## Security Review

The project undergoes a security review process to mitigate potential vulnerabilities such as prompt injection, malicious repository names, URL injection, and unsafe parsing of API responses.

## Documentation Structure

- `README.md`: Project overview, installation, usage.
- `SKILL.md`: Claude/ChatGPT skill definition.
- `CONTRIBUTING.md`: Guidelines for contributing to the project.
- `CHANGELOG.md`: Records of all notable changes to the project.
- `docs/`: Detailed documentation including architecture, developer guide, troubleshooting, and API reference.
- `examples/`: Code examples for various use cases.

## Contributing

We welcome contributions! Please see `CONTRIBUTING.md` for details on how to get started.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Connect with me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/ehsassethi)
